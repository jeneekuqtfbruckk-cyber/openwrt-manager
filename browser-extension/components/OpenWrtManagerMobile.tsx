

import { useState, useEffect } from "react"
import { Play, Download, ChevronDown, Activity, CheckCircle2, XCircle, Clock } from "lucide-react"

interface ScanResult {
    id: number
    address: string
    status: "success" | "failed" | "pending"
    username: string
    password: string
    details: string
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

export default function OpenWrtManagerMobile() {
    const [targets, setTargets] = useState("")
    const [threads, setThreads] = useState(50)
    const [showThreadsMenu, setShowThreadsMenu] = useState(false)
    const [isScanning, setIsScanning] = useState(false)
    const [results, setResults] = useState<ScanResult[]>([])
    const [showExportMenu, setShowExportMenu] = useState(false)
    const [activeTab, setActiveTab] = useState<"scan" | "results">("scan")
    const [toast, setToast] = useState<{ show: boolean; message: string }>({ show: false, message: "" })
    const [sortConfig, setSortConfig] = useState<{ key: string; direction: "asc" | "desc" } | null>(null)
    const [selectedIds, setSelectedIds] = useState<Set<number>>(new Set())

    // Success/Failed counts from state or calculation
    const [stats, setStats] = useState({ success: 0, failed: 0 })

    useEffect(() => {
        // Initial load
        if (typeof chrome !== 'undefined' && chrome.storage) {
            chrome.storage.local.get(['local:scan_results', 'local:scan_state'], (data) => {
                if (data['local:scan_results']) {
                    setResults(data['local:scan_results'] as ScanResult[]);
                }
                if (data['local:scan_state']) {
                    const state = data['local:scan_state'] as ScanState;
                    setIsScanning(state.isScanning);
                    if (state.targets && !targets) setTargets(state.targets); // Only restore if empty
                    if (state.progress) setStats({ success: state.progress.success, failed: state.progress.failed });
                }
            });

            // Listen for updates
            const listener = (changes: { [key: string]: chrome.storage.StorageChange }, areaName: string) => {
                if (areaName === 'local') {
                    if (changes['local:scan_results']) {
                        setResults((changes['local:scan_results'].newValue || []) as ScanResult[]);
                    }
                    if (changes['local:scan_state']) {
                        const state = changes['local:scan_state'].newValue as ScanState;
                        setIsScanning(state.isScanning);
                        if (state.progress) setStats({ success: state.progress.success, failed: state.progress.failed });
                    }
                }
            };
            chrome.storage.onChanged.addListener(listener);
            return () => chrome.storage.onChanged.removeListener(listener);
        }
    }, []);

    const showToast = (message: string) => {
        setToast({ show: true, message })
        setTimeout(() => setToast({ show: false, message: "" }), 2000)
    }

    const handleSort = (key: string) => {
        let direction: "asc" | "desc" = "asc"
        if (sortConfig && sortConfig.key === key && sortConfig.direction === "asc") {
            direction = "desc"
        }
        setSortConfig({ key, direction })
    }

    const sortedResults = [...results].sort((a, b) => {
        if (!sortConfig) return 0

        let aValue: any = a[sortConfig.key as keyof ScanResult]
        let bValue: any = b[sortConfig.key as keyof ScanResult]

        // Special handling for IP sorting
        if (sortConfig.key === 'address') {
            const ipToNum = (ip: string) => {
                const parts = ip.replace(/^http(s)?:\/\//, '').split(':')[0].split('.').map(Number);
                return parts.length === 4 ? (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3] : 0;
            };
            aValue = ipToNum(a.address);
            bValue = ipToNum(b.address);
        }

        if (aValue < bValue) return sortConfig.direction === "asc" ? -1 : 1
        if (aValue > bValue) return sortConfig.direction === "asc" ? 1 : -1
        return 0
    })

    const handleRowClick = (e: React.MouseEvent, id: number) => {
        if (e.ctrlKey || e.metaKey) {
            const newSelected = new Set(selectedIds)
            if (newSelected.has(id)) {
                newSelected.delete(id)
            } else {
                newSelected.add(id)
            }
            setSelectedIds(newSelected)
        } else {
            // If not holding Ctrl, select only this one (standard behavior)
            // Or maybe user wants toggle? Standard is select single.
            setSelectedIds(new Set([id]))
        }
    }

    const handleContextMenu = (e: React.MouseEvent, result: ScanResult) => {
        e.preventDefault()

        // If the clicked row is NOT in selection, select it (exclusive)
        let currentSelection = new Set(selectedIds)
        if (!currentSelection.has(result.id)) {
            currentSelection = new Set([result.id])
            setSelectedIds(currentSelection)
        }

        // Copy ALL selected items
        const selectedItems = results.filter(r => currentSelection.has(r.id))
        const text = selectedItems.map(r =>
            `${r.address}\t${r.username}\t${r.password}\t${r.details}`
        ).join('\n')

        navigator.clipboard.writeText(text).then(() => {
            showToast(`已复制 ${selectedItems.length} 条记录`)
        })
    }

    const handleStartScan = () => {
        if (!targets.trim()) return;

        // Clear previous results visually immediately for better UX
        setResults([]);
        setStats({ success: 0, failed: 0 });

        // Send message to background
        if (typeof chrome !== 'undefined' && chrome.runtime) {
            chrome.runtime.sendMessage({
                type: 'START_SCAN',
                targets: targets,
                threads: threads
            });
        }

        setActiveTab("results");
        setIsScanning(true);
    }

    const getStatusIcon = (status: ScanResult["status"]) => {
        switch (status) {
            case "success":
                return <CheckCircle2 className="w-4 h-4 text-[#34c759]" />
            case "failed":
                return <XCircle className="w-4 h-4 text-[#ff3b30]" />
            case "pending":
                return <Clock className="w-4 h-4 text-[#ff9500] animate-pulse" />
        }
    }

    const threadOptions = [50, 100, 200]

    return (
        <div className="h-screen flex flex-col bg-[#f5f5f7]">
            {(showThreadsMenu || showExportMenu) && (
                <div
                    className="fixed inset-0 z-30 bg-black/20"
                    onClick={() => {
                        setShowThreadsMenu(false)
                        setShowExportMenu(false)
                    }}
                />
            )}

            <div className="h-14 bg-gradient-to-b from-[#e8e8e8] to-[#d4d4d4] border-b border-[#b8b8b8] flex items-center justify-center px-4 relative">
                <div className="absolute left-4 flex items-center gap-1.5">
                    <div className="w-2.5 h-2.5 rounded-full bg-[#ff5f57]" />
                    <div className="w-2.5 h-2.5 rounded-full bg-[#febc2e]" />
                    <div className="w-2.5 h-2.5 rounded-full bg-[#28c840]" />
                </div>
                <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-[#4d4d4d]">OpenWrt Manager</span>
                    <span className="text-xs text-[#8e8e8e]">v2.0</span>
                </div>

            </div>

            {/* Toast Notification */}
            {toast.show && (
                <div className="fixed bottom-20 left-1/2 -translate-x-1/2 px-4 py-2 bg-black/75 backdrop-blur-md text-white text-xs rounded-full shadow-lg z-50 animate-in fade-in zoom-in duration-200">
                    {toast.message}
                </div>
            )}

            <div className="flex-1 overflow-hidden">
                {activeTab === "scan" ? (
                    <div className="h-full flex flex-col p-4">
                        <div className="flex-1 min-h-0 flex flex-col mb-4 bg-white/50 rounded-lg border border-[#c7c7c7] overflow-hidden">
                            <textarea
                                value={targets}
                                onChange={(e) => setTargets(e.target.value)}
                                placeholder="输入 IP 地址，每行一个...&#10;例如：&#10;192.168.1.1&#10;192.168.1.2"
                                className="flex-1 w-full p-3 text-xs font-mono text-[#1d1d1f] placeholder:text-[#8e8e8e] bg-transparent resize-none leading-relaxed focus:outline-none"
                            />
                        </div>

                        <div className="bg-white rounded-lg border border-[#c7c7c7] p-3 mb-4 shrink-0">
                            <h3 className="text-xs font-semibold text-[#8e8e8e] uppercase tracking-wide mb-2">统计概览</h3>
                            {results.length === 0 ? (
                                <div className="text-xs text-[#8e8e8e]">待开始探测...</div>
                            ) : (
                                <div className="grid grid-cols-3 gap-2">
                                    <div className="text-center">
                                        <div className="text-lg font-semibold text-[#34c759] tabular-nums">{stats.success}</div>
                                        <div className="text-[10px] text-[#8e8e8e]">成功</div>
                                    </div>
                                    <div className="text-center">
                                        <div className="text-lg font-semibold text-[#ff3b30] tabular-nums">{stats.failed}</div>
                                        <div className="text-[10px] text-[#8e8e8e]">失败</div>
                                    </div>
                                    <div className="text-center">
                                        <div className="text-lg font-semibold text-[#1d1d1f] tabular-nums">{results.length}</div>
                                        <div className="text-[10px] text-[#8e8e8e]">总计</div>
                                    </div>
                                </div>
                            )}
                        </div>

                        <div className="flex items-center gap-2 shrink-0">
                            <div className="relative flex-1">
                                <button
                                    onClick={() => setShowThreadsMenu(!showThreadsMenu)}
                                    className="h-10 px-3 w-full bg-white hover:bg-[#fafafa] border border-[#c7c7c7] text-[#1d1d1f] text-xs rounded-lg transition-all duration-150 flex items-center justify-between gap-2 active:scale-[0.98]"
                                >
                                    <span className="text-[#8e8e8e]">并发</span>
                                    <span className="font-medium tabular-nums">{threads}</span>
                                    <ChevronDown
                                        className={`w-3 h-3 text-[#8e8e8e] transition-transform duration-150 ${showThreadsMenu ? "rotate-180" : ""}`}
                                    />
                                </button>
                                {showThreadsMenu && (
                                    <div className="absolute bottom-full left-0 mb-1 bg-white rounded-lg shadow-xl border border-[#c7c7c7] overflow-hidden z-40">
                                        {threadOptions.map((option) => (
                                            <button
                                                key={option}
                                                onClick={() => {
                                                    setThreads(option)
                                                    setShowThreadsMenu(false)
                                                }}
                                                className={`w-full px-4 py-2 text-xs text-left transition-colors flex items-center justify-between gap-4 ${threads === option ? "bg-[#0071e3] text-white" : "text-[#1d1d1f] hover:bg-[#f5f5f7]"
                                                    }`}
                                            >
                                                <span>{option} 线程</span>
                                                {threads === option && <span>✓</span>}
                                            </button>
                                        ))}
                                    </div>
                                )}
                            </div>

                            <button
                                onClick={handleStartScan}
                                disabled={isScanning || !targets.trim()}
                                className="flex-1 h-10 bg-[#0071e3] hover:bg-[#0077ed] disabled:bg-[#8e8e8e] text-white text-xs font-medium rounded-lg transition-all duration-150 flex items-center justify-center gap-1.5 disabled:cursor-not-allowed active:scale-[0.98]"
                            >
                                {isScanning ? (
                                    <>
                                        <div className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                        <span>扫描中...</span>
                                    </>
                                ) : (
                                    <>
                                        <Play className="w-3 h-3 fill-current" />
                                        <span>开始探测</span>
                                    </>
                                )}
                            </button>
                        </div>
                    </div>
                ) : (
                    <div className="h-full flex flex-col">
                        <div className="bg-[#fafafa] border-b border-[#d1d1d6] px-3 py-2 flex items-center justify-between shrink-0">
                            <div className="flex items-center gap-2">
                                <h2 className="text-[10px] font-semibold text-[#8e8e8e] uppercase tracking-wide">结果</h2>
                                {results.length > 0 && <span className="text-[10px] text-[#8e8e8e]">({results.length})</span>}
                            </div>
                            <div className="relative">
                                <button
                                    onClick={() => setShowExportMenu(!showExportMenu)}
                                    className="h-7 px-2 bg-white hover:bg-[#f5f5f7] border border-[#c7c7c7] text-[#1d1d1f] text-[10px] rounded hover:border-[#8e8e8e] transition-all flex items-center gap-1"
                                >
                                    <Download className="w-3 h-3" />
                                    <span>导出</span>
                                </button>
                                {showExportMenu && (
                                    <div className="absolute top-full right-0 mt-1 bg-white rounded-lg shadow-xl border border-[#c7c7c7] overflow-hidden z-40 min-w-[100px]">
                                        <button className="w-full px-3 py-2 text-xs text-[#1d1d1f] hover:bg-[#0071e3] hover:text-white text-left">csv</button>
                                        <button className="w-full px-3 py-2 text-xs text-[#1d1d1f] hover:bg-[#0071e3] hover:text-white text-left">json</button>
                                        <button className="w-full px-3 py-2 text-xs text-[#1d1d1f] hover:bg-[#0071e3] hover:text-white text-left">txt</button>
                                    </div>
                                )}
                            </div>
                        </div>

                        <div className="flex-1 overflow-hidden flex flex-col min-h-0">
                            {/* Table Header */}
                            <div className="flex items-center gap-3 px-3 py-2 bg-[#f5f5f7] border-b border-[#e5e5e5] text-[10px] font-semibold text-[#8e8e8e] select-none shrink-0">
                                <div
                                    className="flex-1 cursor-pointer hover:text-[#1d1d1f] flex items-center gap-1 transition-colors"
                                    onClick={() => handleSort('address')}
                                >
                                    目标地址
                                    {sortConfig?.key === 'address' && <ChevronDown className={`w-3 h-3 transition-transform ${sortConfig.direction === 'asc' ? 'rotate-180' : ''}`} />}
                                </div>
                                <div
                                    className="w-20 cursor-pointer hover:text-[#1d1d1f] flex items-center gap-1 transition-colors"
                                    onClick={() => handleSort('status')}
                                >
                                    状态
                                    {sortConfig?.key === 'status' && <ChevronDown className={`w-3 h-3 transition-transform ${sortConfig.direction === 'asc' ? 'rotate-180' : ''}`} />}
                                </div>
                            </div>

                            <div className="flex-1 overflow-y-auto min-h-0">
                                {sortedResults.length === 0 ? (
                                    <div className="flex flex-col items-center justify-center h-full text-center px-4">
                                        <Activity className="w-8 h-8 text-[#c7c7c7] mb-2" />
                                        <p className="text-xs text-[#8e8e8e]">暂无结果</p>
                                    </div>
                                ) : (
                                    <div className="divide-y divide-[#e5e5e5]">
                                        {sortedResults.map((result) => (
                                            <div
                                                key={result.id}
                                                className={`p-3 transition-colors flex items-center justify-between gap-3 text-xs cursor-default select-none group 
                                                    ${selectedIds.has(result.id) ? 'bg-[#0071e3]/10 hover:bg-[#0071e3]/15' : 'hover:bg-[#f5f5f7]'}
                                                `}
                                                onClick={(e) => handleRowClick(e, result.id)}
                                                onContextMenu={(e) => handleContextMenu(e, result)}
                                            >
                                                <div className="min-w-0 flex-1">
                                                    <div className="flex items-baseline justify-between mb-0.5">
                                                        <span className="font-bold text-[#1d1d1f] font-mono truncate mr-2">{result.address}</span>
                                                        <span className="text-[10px] text-[#8e8e8e] shrink-0 truncate max-w-[120px]">{result.details}</span>
                                                    </div>

                                                    {result.status === "success" && (
                                                        <div className="flex items-center gap-3 text-[#555] font-mono text-[10px]">
                                                            <span className="flex items-center gap-1">
                                                                <span className="text-[#999]">用户:</span> {result.username}
                                                            </span>
                                                            <span className="flex items-center gap-1">
                                                                <span className="text-[#999]">密码:</span> {result.password}
                                                            </span>
                                                        </div>
                                                    )}
                                                    {result.status === "failed" && (
                                                        <div className="text-[10px] text-[#ff3b30]">{result.details}</div>
                                                    )}
                                                </div>

                                                <div className="shrink-0">
                                                    {getStatusIcon(result.status)}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                )}
            </div>

            <div className="h-16 bg-white border-t border-[#d1d1d6] flex items-center justify-around px-4">
                <button
                    onClick={() => setActiveTab("scan")}
                    className={`flex-1 flex flex-col items-center gap-1 py-2 transition-all relative ${activeTab === "scan" ? "text-[#0071e3]" : "text-[#8e8e8e]"
                        }`}
                >
                    <Play className={`w-5 h-5 ${activeTab === "scan" ? "text-[#0071e3]" : "text-[#8e8e8e]"}`} />
                    <span className={`text-xs font-medium ${activeTab === "scan" ? "text-[#1d1d1f]" : "text-[#8e8e8e]"}`}>
                        输入页
                    </span>
                    {activeTab === "scan" && (
                        <div className="absolute bottom-0 left-1/4 right-1/4 h-0.5 bg-[#0071e3] rounded-full" />
                    )}
                </button>
                <button
                    onClick={() => setActiveTab("results")}
                    className={`flex-1 flex flex-col items-center gap-1 py-2 transition-all relative ${activeTab === "results" ? "text-[#0071e3]" : "text-[#8e8e8e]"
                        }`}
                >
                    <Activity className={`w-5 h-5 ${activeTab === "results" ? "text-[#0071e3]" : "text-[#8e8e8e]"}`} />
                    <span className={`text-xs font-medium ${activeTab === "results" ? "text-[#1d1d1f]" : "text-[#8e8e8e]"}`}>
                        输出页
                    </span>
                    {activeTab === "results" && (
                        <div className="absolute bottom-0 left-1/4 right-1/4 h-0.5 bg-[#0071e3] rounded-full" />
                    )}
                    {results.length > 0 && (
                        <span className="absolute top-0 right-1/4 bg-[#ff3b30] text-white text-[10px] font-semibold rounded-full w-5 h-5 flex items-center justify-center">
                            {results.length}
                        </span>
                    )}
                </button>
            </div>
        </div>
    )
}
