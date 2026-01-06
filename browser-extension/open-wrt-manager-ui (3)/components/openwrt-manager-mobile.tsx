"use client"

import { useState } from "react"
import { Play, Download, ChevronDown, Activity, CheckCircle2, XCircle, Clock } from "lucide-react"

interface ScanResult {
  id: number
  address: string
  status: "success" | "failed" | "pending"
  username: string
  password: string
  details: string
}

export default function OpenWrtManagerMobile() {
  const [targets, setTargets] = useState("")
  const [threads, setThreads] = useState(50)
  const [showThreadsMenu, setShowThreadsMenu] = useState(false)
  const [isScanning, setIsScanning] = useState(false)
  const [results, setResults] = useState<ScanResult[]>([])
  const [showExportMenu, setShowExportMenu] = useState(false)
  const [activeTab, setActiveTab] = useState<"scan" | "results">("scan")

  const handleStartScan = () => {
    if (!targets.trim()) return
    setIsScanning(true)

    setTimeout(() => {
      const mockResults: ScanResult[] = [
        {
          id: 1,
          address: "192.168.1.1",
          status: "success",
          username: "root",
          password: "admin",
          details: "OpenWrt 22.03",
        },
        { id: 2, address: "192.168.1.2", status: "failed", username: "-", password: "-", details: "连接超时" },
        {
          id: 3,
          address: "192.168.1.3",
          status: "success",
          username: "admin",
          password: "password",
          details: "OpenWrt 21.02",
        },
        { id: 4, address: "192.168.1.4", status: "pending", username: "-", password: "-", details: "扫描中..." },
      ]
      setResults(mockResults)
      setIsScanning(false)
      setActiveTab("results")
    }, 2000)
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

  const successCount = results.filter((r) => r.status === "success").length
  const failedCount = results.filter((r) => r.status === "failed").length

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
        <div className="absolute right-4">
          <span className="text-xs text-[#4d4d4d]">
            {new Date().toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" })}
          </span>
        </div>
      </div>

      <div className="flex-1 overflow-hidden">
        {activeTab === "scan" ? (
          <div className="h-full flex flex-col p-4">
            <div className="flex-1 flex flex-col mb-4">
              <div className="flex items-center justify-between mb-2">
                <h2 className="text-xs font-semibold text-[#8e8e8e] uppercase tracking-wide">目标</h2>
                {targets.trim() && (
                  <span className="text-xs text-[#8e8e8e]">
                    {targets.trim().split("\n").filter(Boolean).length} 个地址
                  </span>
                )}
              </div>
              <textarea
                value={targets}
                onChange={(e) => setTargets(e.target.value)}
                placeholder="输入 IP 地址，每行一个...&#10;例如：&#10;192.168.1.1&#10;192.168.1.2"
                className="flex-1 w-full px-3 py-3 text-sm text-[#1d1d1f] placeholder:text-[#8e8e8e] bg-white rounded-lg border border-[#c7c7c7] focus:outline-none focus:border-[#0071e3] focus:ring-2 focus:ring-[#0071e3]/20 resize-none leading-relaxed"
              />
            </div>

            <div className="bg-white rounded-lg border border-[#c7c7c7] p-4 mb-4">
              <h3 className="text-xs font-semibold text-[#8e8e8e] uppercase tracking-wide mb-3">统计概览</h3>
              {results.length === 0 ? (
                <div className="text-sm text-[#8e8e8e]">待开始探测...</div>
              ) : (
                <div className="grid grid-cols-3 gap-3">
                  <div className="text-center">
                    <div className="text-2xl font-semibold text-[#34c759] tabular-nums">{successCount}</div>
                    <div className="text-xs text-[#8e8e8e] mt-1">成功</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-semibold text-[#ff3b30] tabular-nums">{failedCount}</div>
                    <div className="text-xs text-[#8e8e8e] mt-1">失败</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-semibold text-[#1d1d1f] tabular-nums">{results.length}</div>
                    <div className="text-xs text-[#8e8e8e] mt-1">总计</div>
                  </div>
                </div>
              )}
            </div>

            <div className="flex items-center gap-2">
              <div className="relative">
                <button
                  onClick={() => setShowThreadsMenu(!showThreadsMenu)}
                  className="h-12 px-4 bg-white hover:bg-[#fafafa] border border-[#c7c7c7] text-[#1d1d1f] text-sm rounded-lg transition-all duration-150 flex items-center gap-2 active:scale-[0.98]"
                >
                  <span className="text-[#8e8e8e]">并发</span>
                  <span className="font-medium tabular-nums">{threads}</span>
                  <ChevronDown
                    className={`w-4 h-4 text-[#8e8e8e] transition-transform duration-150 ${showThreadsMenu ? "rotate-180" : ""}`}
                  />
                </button>
                {showThreadsMenu && (
                  <div className="absolute bottom-full left-0 mb-2 bg-white rounded-lg shadow-xl border border-[#c7c7c7] overflow-hidden z-40">
                    {threadOptions.map((option) => (
                      <button
                        key={option}
                        onClick={() => {
                          setThreads(option)
                          setShowThreadsMenu(false)
                        }}
                        className={`w-full px-4 py-3 text-sm text-left transition-colors flex items-center justify-between gap-4 ${
                          threads === option ? "bg-[#0071e3] text-white" : "text-[#1d1d1f] hover:bg-[#f5f5f7]"
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
                className="flex-1 h-12 bg-[#0071e3] hover:bg-[#0077ed] disabled:bg-[#8e8e8e] text-white text-sm font-medium rounded-lg transition-all duration-150 flex items-center justify-center gap-2 disabled:cursor-not-allowed active:scale-[0.98]"
              >
                {isScanning ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    <span>扫描中...</span>
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4 fill-current" />
                    <span>开始探测</span>
                  </>
                )}
              </button>
            </div>
          </div>
        ) : (
          <div className="h-full flex flex-col">
            <div className="bg-[#fafafa] border-b border-[#d1d1d6] px-4 py-3 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <h2 className="text-xs font-semibold text-[#8e8e8e] uppercase tracking-wide">结果</h2>
                {results.length > 0 && <span className="text-xs text-[#8e8e8e]">({results.length})</span>}
              </div>
              <div className="relative">
                <button
                  onClick={() => setShowExportMenu(!showExportMenu)}
                  className="h-8 px-3 bg-white hover:bg-[#f5f5f7] border border-[#c7c7c7] text-[#1d1d1f] text-xs rounded-md transition-all duration-150 flex items-center gap-1.5 active:scale-[0.98]"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>导出</span>
                  <ChevronDown
                    className={`w-3.5 h-3.5 transition-transform duration-150 ${showExportMenu ? "rotate-180" : ""}`}
                  />
                </button>
                {showExportMenu && (
                  <div className="absolute top-full right-0 mt-1 bg-white rounded-lg shadow-xl border border-[#c7c7c7] overflow-hidden z-40 min-w-[130px]">
                    <button className="w-full px-3 py-2.5 text-sm text-[#1d1d1f] hover:bg-[#0071e3] hover:text-white text-left transition-colors">
                      导出为 CSV
                    </button>
                    <button className="w-full px-3 py-2.5 text-sm text-[#1d1d1f] hover:bg-[#0071e3] hover:text-white text-left transition-colors">
                      导出为 JSON
                    </button>
                    <button className="w-full px-3 py-2.5 text-sm text-[#1d1d1f] hover:bg-[#0071e3] hover:text-white text-left transition-colors">
                      导出为 TXT
                    </button>
                  </div>
                )}
              </div>
            </div>

            <div className="flex-1 overflow-auto">
              {results.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-center px-4">
                  <Activity className="w-12 h-12 text-[#c7c7c7] mb-3" />
                  <p className="text-base font-medium text-[#1d1d1f] mb-1">暂无结果</p>
                  <p className="text-sm text-[#8e8e8e]">输入目标地址并点击开始探测</p>
                </div>
              ) : (
                <div className="divide-y divide-[#e5e5e5]">
                  {results.map((result) => (
                    <div key={result.id} className="p-4 hover:bg-[#f5f5f7] transition-colors">
                      <div className="flex items-start justify-between mb-2">
                        <span className="text-sm font-mono font-medium text-[#1d1d1f]">{result.address}</span>
                        <div className="flex items-center gap-1.5">{getStatusIcon(result.status)}</div>
                      </div>
                      {result.status === "success" && (
                        <div className="space-y-1.5 mb-2">
                          <div className="flex items-center gap-2">
                            <span className="text-xs text-[#8e8e8e] w-12">用户名</span>
                            <span className="text-sm font-mono text-[#1d1d1f]">{result.username}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <span className="text-xs text-[#8e8e8e] w-12">密码</span>
                            <span className="text-sm font-mono text-[#1d1d1f]">{result.password}</span>
                          </div>
                        </div>
                      )}
                      <div className="text-xs text-[#8e8e8e]">{result.details}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      <div className="h-16 bg-white border-t border-[#d1d1d6] flex items-center justify-around px-4">
        <button
          onClick={() => setActiveTab("scan")}
          className={`flex-1 flex flex-col items-center gap-1 py-2 transition-all relative ${
            activeTab === "scan" ? "text-[#0071e3]" : "text-[#8e8e8e]"
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
          className={`flex-1 flex flex-col items-center gap-1 py-2 transition-all relative ${
            activeTab === "results" ? "text-[#0071e3]" : "text-[#8e8e8e]"
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
