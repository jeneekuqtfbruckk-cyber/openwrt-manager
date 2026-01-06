import React, { useState } from 'react';
import { Plus, Server, ChevronRight, Activity, Trash2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '../utils/cn';
import { savedRouters, type RouterConfig } from '../utils/storage';

// Map stored config to view model
interface Router extends RouterConfig {
    status: 'online' | 'offline';
}

interface RouterListProps {
    onSelect: (router: Router) => void;
}

export function RouterList({ onSelect }: RouterListProps) {
    // Mock initial data - later this will come from storage
    const [routers, setRouters] = useState<Router[]>([]);
    const [newIp, setNewIp] = useState('');
    const [isAdding, setIsAdding] = useState(false);

    React.useEffect(() => {
        // Load initial and map to Router type
        savedRouters.getValue().then(configs => {
            setRouters(configs.map(c => ({ ...c, status: 'offline' as const })));
        });

        // Watch for changes
        const unwatch = savedRouters.watch(configs => {
            setRouters(configs.map(c => ({ ...c, status: 'offline' as const })));
        });
        return () => unwatch();
    }, []);

    const handleAdd = async () => {
        if (!newIp) return;

        // Basic IP validation?

        const newRouter: Router = {
            id: Date.now().toString(),
            name: newIp, // Default name is IP
            ip: newIp,
            status: 'offline', // Default
        };

        const current = await savedRouters.getValue();
        await savedRouters.setValue([...current, newRouter]);

        setNewIp('');
        setIsAdding(false);
    };

    return (
        <div className="h-full flex flex-col">
            <div className="mb-4 flex justify-between items-center">
                <div>
                    <h1 className="text-lg font-semibold text-foreground">My Routers</h1>
                    <p className="text-xs text-muted-foreground">{routers.length} devices managed</p>
                </div>
                <button
                    onClick={() => setIsAdding(!isAdding)}
                    className="p-2 hover:bg-muted rounded-full transition-colors text-primary"
                >
                    <Plus className="w-5 h-5" />
                </button>
            </div>

            <AnimatePresence>
                {isAdding && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        className="overflow-hidden mb-4"
                    >
                        <div className="flex gap-2">
                            <input
                                type="text"
                                placeholder="Enter IP (e.g., 192.168.1.1)"
                                className="flex-1 bg-muted/50 border border-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                                value={newIp}
                                onChange={(e) => setNewIp(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleAdd()}
                            />
                            <button
                                onClick={handleAdd}
                                className="bg-primary text-primary-foreground px-4 py-2 rounded-lg text-sm font-medium"
                            >
                                Add
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            <div className="flex-1 overflow-y-auto space-y-2 pr-1">
                {routers.map((router) => (
                    <motion.div
                        key={router.id}
                        layoutId={router.id}
                        onClick={() => onSelect(router)}
                        className="group flex items-center justify-between p-3 bg-card/50 hover:bg-card border border-border/50 hover:border-border rounded-xl cursor-pointer transition-all hover:shadow-sm"
                    >
                        <div className="flex items-center gap-3">
                            <div className={cn(
                                "w-10 h-10 rounded-full flex items-center justify-center bg-muted",
                                router.status === 'online' ? "text-primary bg-primary/10" : "text-muted-foreground"
                            )}>
                                <Server className="w-5 h-5" />
                            </div>
                            <div>
                                <h3 className="text-sm font-medium text-foreground">{router.name}</h3>
                                <div className="flex items-center gap-1.5">
                                    <span className={cn(
                                        "w-1.5 h-1.5 rounded-full",
                                        router.status === 'online' ? "bg-green-500" : "bg-red-500"
                                    )} />
                                    <p className="text-xs text-muted-foreground">{router.ip}</p>
                                </div>
                            </div>
                        </div>
                        <ChevronRight className="w-4 h-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
                    </motion.div>
                ))}
            </div>
        </div>
    );
}
