export class UBusClient {
    private baseUrl: string;
    private token: string | null = null;

    constructor(ip: string, token?: string) {
        this.baseUrl = ip.startsWith('http') ? ip : `http://${ip}`;
        this.token = token || null;
    }

    async rpc(object: string, method: string, params: any = {}) {
        const url = `${this.baseUrl}/ubus`;
        const payload = {
            jsonrpc: '2.0',
            id: Date.now(),
            method: 'call',
            params: [this.token || '00000000000000000000000000000000', object, method, params],
        };

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status}`);
            }

            const data = await response.json();
            if (data.error) {
                throw new Error(`RPC Error: ${JSON.stringify(data.error)}`);
            }

            return data.result?.[1]; // ubus returns [0, {result}]
        } catch (error) {
            console.warn('UBus Call Failed:', error);
            throw error;
        }
    }

    async login(username: string = 'root', password: string) {
        // Session login logic implementation
        // Depending on router version, this might use 'session' 'login'
        const result = await this.rpc('session', 'login', { username, password });
        if (result && result.ubus_rpc_session) {
            this.token = result.ubus_rpc_session;
            return this.token;
        }
        throw new Error('Login failed');
    }

    async checkOnline(): Promise<boolean> {
        try {
            // Simple unchecked call to see if endpoint is reachable
            // Often 'system' 'board' requires no auth or minimal rights, 
            // but without token it acts as a reachability test mostly.
            // Better: try to fetch the ubus endpoint options
            await fetch(`${this.baseUrl}/ubus`, { method: 'OPTIONS' });
            return true;
        } catch (e) {
            return false;
        }
    }

    // System stats
    async getSystemInfo() {
        return this.rpc('system', 'info');
    }
}
