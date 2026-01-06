// 使用标准的 Chrome Storage API 而不是 wxt/storage
export interface RouterConfig {
    id: string;
    name: string;
    ip: string;
    username?: string;
    password?: string;
    token?: string;
    lastSeen?: number;
}

const STORAGE_KEYS = {
    ROUTERS: 'routers',
    ACTIVE_ROUTER_ID: 'activeRouterId',
};

export const savedRouters = {
    async getValue(): Promise<RouterConfig[]> {
        const result = await chrome.storage.local.get(STORAGE_KEYS.ROUTERS);
        return result[STORAGE_KEYS.ROUTERS] || [];
    },

    async setValue(value: RouterConfig[]): Promise<void> {
        await chrome.storage.local.set({ [STORAGE_KEYS.ROUTERS]: value });
    },

    watch(callback: (value: RouterConfig[]) => void): () => void {
        const listener = (changes: { [key: string]: chrome.storage.StorageChange }) => {
            if (changes[STORAGE_KEYS.ROUTERS]) {
                callback(changes[STORAGE_KEYS.ROUTERS].newValue || []);
            }
        };
        chrome.storage.onChanged.addListener(listener);
        return () => chrome.storage.onChanged.removeListener(listener);
    },
};

export const activeRouterId = {
    async getValue(): Promise<string | null> {
        const result = await chrome.storage.local.get(STORAGE_KEYS.ACTIVE_ROUTER_ID);
        return result[STORAGE_KEYS.ACTIVE_ROUTER_ID] || null;
    },

    async setValue(value: string | null): Promise<void> {
        await chrome.storage.local.set({ [STORAGE_KEYS.ACTIVE_ROUTER_ID]: value });
    },
};
