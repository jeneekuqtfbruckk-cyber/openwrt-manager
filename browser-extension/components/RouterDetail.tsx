import React from 'react';
import { Activity, Wifi, HardDrive, Cpu, ArrowLeft, Settings } from 'lucide-react';

interface Router {
    id: string;
    name: string;
    ip: string;
    status: 'online' | 'offline';
}

interface RouterDetailProps {
    router: Router;
    onBack: () => void;
}

export function RouterDetail({ router, onBack }: RouterDetailProps) {
    return (
        <div className="h-full flex flex-col">
            {/* Header */}
            <div className="mb-4 flex items-center justify-between">
                <button
                    onClick={onBack}
                    className="p-2 -ml-2 hover:bg-muted/50 rounded-full transition-colors text-muted-foreground hover:text-foreground"
                >
                    <ArrowLeft className="w-5 h-5" />
                </button>
                <div className="flex flex-col items-center">
                    <h1 className="text-sm font-semibold text-foreground">{router.name}</h1>
                    <span className="text-xs text-muted-foreground flex items-center gap-1">
                        <span className="w-1.5 h-1.5 rounded-full bg-green-500" />
                        {router.ip}
                    </span>
                </div>
                <button className="p-2 -mr-2 text-muted-foreground hover:text-foreground">
                    <Settings className="w-5 h-5" />
                </button>
            </div>

            {/* Stats Grid - Reusing the previous design */}
            <div className="grid grid-cols-2 gap-3 mb-4">
                <div className="bg-card/80 backdrop-blur-sm border border-border rounded-xl p-4 shadow-sm">
                    <div className="flex items-center gap-2 mb-2">
                        <Cpu className="w-4 h-4 text-primary" />
                        <span className="text-xs font-medium text-muted-foreground">CPU</span>
                    </div>
                    <p className="text-2xl font-bold text-foreground">23%</p>
                </div>

                <div className="bg-card/80 backdrop-blur-sm border border-border rounded-xl p-4 shadow-sm">
                    <div className="flex items-center gap-2 mb-2">
                        <HardDrive className="w-4 h-4 text-primary" />
                        <span className="text-xs font-medium text-muted-foreground">内存</span>
                    </div>
                    <p className="text-2xl font-bold text-foreground">45%</p>
                </div>

                <div className="bg-card/80 backdrop-blur-sm border border-border rounded-xl p-4 col-span-2 shadow-sm">
                    <div className="flex items-center gap-2 mb-3">
                        <Wifi className="w-4 h-4 text-primary" />
                        <span className="text-xs font-medium text-muted-foreground">实时网络</span>
                    </div>
                    <div className="flex justify-between items-center px-2">
                        <div>
                            <p className="text-xs text-muted-foreground mb-1">上传</p>
                            <p className="text-lg font-semibold text-foreground flex items-baseline gap-1">
                                1.2 <span className="text-xs font-normal text-muted-foreground">MB/s</span>
                            </p>
                        </div>
                        <div className="h-8 w-px bg-border/50" />
                        <div className="text-right">
                            <p className="text-xs text-muted-foreground mb-1">下载</p>
                            <p className="text-lg font-semibold text-foreground flex items-baseline gap-1 justify-end">
                                5.8 <span className="text-xs font-normal text-muted-foreground">MB/s</span>
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Action Button */}
            <button className="w-full mt-auto bg-primary hover:bg-primary/90 text-primary-foreground rounded-xl py-3 text-sm font-medium transition-colors shadow-sm">
                进入管理后台
            </button>
        </div>
    );
}
