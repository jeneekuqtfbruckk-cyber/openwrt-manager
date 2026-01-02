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

export default function OpenWrtManager() {
  const [targets, setTargets] = useState("")
  const [threads, setThreads] = useState(50)
  const [isScanning, setIsScanning] = useState(false)
  const [results, setResults] = useState<ScanResult[]>([])
  const [showExportMenu, setShowExportMenu] = useState(false)

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
    }, 2000)
  }

  const getStatusIcon = (status: ScanResult["status"]) => {
    switch (status) {
      case "success":
        return <CheckCircle2 className="w-3.5 h-3.5 text-[#34c759]" />
      case "failed":
        return <XCircle className="w-3.5 h-3.5 text-[#ff3b30]" />
      case "pending":
        return <Clock className="w-3.5 h-3.5 text-[#ff9500] animate-pulse" />
    }
  }

  const getStatusText = (status: ScanResult["status"]) => {
    switch (status) {
      case "success":
        return "成功"
      case "failed":
        return "失败"
      case "pending":
        return "等待中"
    }
  }

  const successCount = results.filter((r) => r.status === "success").length
  const failedCount = results.filter((r) => r.status === "failed").length
  const pendingCount = results.filter((r) => r.status === "pending").length

  return (
    <div className="min-h-screen bg-[#3a3a3c] p-4 md:p-8 flex items-start justify-center">
      <div className="w-full max-w-[1200px] bg-[#f5f5f7] rounded-[10px] shadow-2xl overflow-hidden border border-[#c7c7c7]">
        <div className="h-[52px] bg-gradient-to-b from-[#e8e8e8] to-[#d4d4d4] border-b border-[#b8b8b8] flex items-center px-4 relative">
          {/* 红绿灯按钮 */}
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-[#ff5f57] border border-[#e0443e]" />
            <div className="w-3 h-3 rounded-full bg-[#febc2e] border border-[#d4a528]" />
            <div className="w-3 h-3 rounded-full bg-[#28c840] border border-[#24a732]" />
          </div>
          {/* 标题 */}
          <div className="absolute left-1/2 -translate-x-1/2 flex items-center gap-2">
            <span className="text-[13px] font-medium text-[#4d4d4d]">OpenWrt Manager</span>
            <span className="text-[11px] text-[#8e8e8e]">v2.0</span>
          </div>
        </div>

        <div className="flex" style={{ height: "calc(100vh - 120px)", minHeight: "500px" }}>
          <div className="w-[280px] bg-[#f5f5f7] border-r border-[#d1d1d6] flex flex-col">
            {/* 目标输入区 */}
            <div className="p-4 border-b border-[#d1d1d6]">
              <h2 className="text-[11px] font-semibold text-[#8e8e8e] uppercase tracking-wide mb-2">目标</h2>
              <textarea
                value={targets}
                onChange={(e) => setTargets(e.target.value)}
                placeholder="输入 IP 地址，每行一个..."
                className="w-full h-28 px-3 py-2 text-[13px] text-[#1d1d1f] placeholder:text-[#8e8e8e] bg-white rounded-[6px] border border-[#c7c7c7] focus:outline-none focus:border-[#0071e3] focus:ring-2 focus:ring-[#0071e3]/20 resize-none leading-relaxed"
              />
            </div>

            {/* 设置区 */}
            <div className="p-4 border-b border-[#d1d1d6]">
              <h2 className="text-[11px] font-semibold text-[#8e8e8e] uppercase tracking-wide mb-3">设置</h2>
              <div className="space-y-4">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-[13px] text-[#1d1d1f]">并发数</label>
                    <span className="text-[13px] text-[#1d1d1f] tabular-nums font-medium">{threads} 线程</span>
                  </div>
                  <input
                    type="range"
                    min="1"
                    max="100"
                    value={threads}
                    onChange={(e) => setThreads(Number(e.target.value))}
                    className="w-full h-[4px] bg-[#d1d1d6] rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:bg-white [&::-webkit-slider-thumb]:border [&::-webkit-slider-thumb]:border-[#b8b8b8] [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:shadow-sm"
                  />
                </div>

                <button
                  onClick={handleStartScan}
                  disabled={isScanning || !targets.trim()}
                  className="w-full h-10 bg-[#1d1d1f] hover:bg-black disabled:bg-[#8e8e8e] text-white text-[13px] font-medium rounded-[6px] transition-all duration-150 flex items-center justify-center gap-2 disabled:cursor-not-allowed active:scale-[0.98]"
                >
                  {isScanning ? (
                    <>
                      <div className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      <span>扫描中...</span>
                    </>
                  ) : (
                    <>
                      <Play className="w-3.5 h-3.5 fill-current" />
                      <span>开始探测</span>
                    </>
                  )}
                </button>

                <div className="relative">
                  <button
                    onClick={() => setShowExportMenu(!showExportMenu)}
                    className="w-full h-10 bg-white hover:bg-[#fafafa] border border-[#c7c7c7] text-[#1d1d1f] text-[13px] font-medium rounded-[6px] transition-all duration-150 flex items-center justify-center gap-2 active:scale-[0.98]"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>导出</span>
                    <ChevronDown
                      className={`w-3.5 h-3.5 transition-transform duration-150 ${showExportMenu ? "rotate-180" : ""}`}
                    />
                  </button>
                  {showExportMenu && (
                    <div className="absolute top-full left-0 right-0 mt-1 bg-white rounded-[6px] shadow-lg border border-[#c7c7c7] overflow-hidden z-10">
                      <button className="w-full px-3 py-2 text-[13px] text-[#1d1d1f] hover:bg-[#0071e3] hover:text-white text-left transition-colors">
                        导出为 CSV
                      </button>
                      <button className="w-full px-3 py-2 text-[13px] text-[#1d1d1f] hover:bg-[#0071e3] hover:text-white text-left transition-colors">
                        导出为 JSON
                      </button>
                      <button className="w-full px-3 py-2 text-[13px] text-[#1d1d1f] hover:bg-[#0071e3] hover:text-white text-left transition-colors">
                        导出为 TXT
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* 概览区 */}
            <div className="p-4 flex-1">
              <h2 className="text-[11px] font-semibold text-[#8e8e8e] uppercase tracking-wide mb-3">概览</h2>
              {results.length === 0 ? (
                <div className="text-[13px] text-[#8e8e8e]">待开始探测...</div>
              ) : (
                <div className="space-y-2">
                  <div className="flex items-center justify-between py-1.5">
                    <span className="text-[13px] text-[#1d1d1f]">成功</span>
                    <span className="text-[13px] font-semibold text-[#34c759] tabular-nums">{successCount}</span>
                  </div>
                  <div className="flex items-center justify-between py-1.5">
                    <span className="text-[13px] text-[#1d1d1f]">失败</span>
                    <span className="text-[13px] font-semibold text-[#ff3b30] tabular-nums">{failedCount}</span>
                  </div>
                  <div className="flex items-center justify-between py-1.5">
                    <span className="text-[13px] text-[#1d1d1f]">等待中</span>
                    <span className="text-[13px] font-semibold text-[#ff9500] tabular-nums">{pendingCount}</span>
                  </div>
                  <div className="pt-2 mt-2 border-t border-[#d1d1d6]">
                    <div className="flex items-center justify-between py-1.5">
                      <span className="text-[13px] text-[#1d1d1f] font-medium">总计</span>
                      <span className="text-[13px] font-semibold text-[#1d1d1f] tabular-nums">{results.length}</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="flex-1 bg-white flex flex-col">
            {/* 结果表头 */}
            <div className="h-10 bg-[#fafafa] border-b border-[#d1d1d6] flex items-center px-4">
              <h2 className="text-[11px] font-semibold text-[#8e8e8e] uppercase tracking-wide">结果</h2>
              {results.length > 0 && <span className="ml-2 text-[11px] text-[#8e8e8e]">({results.length})</span>}
            </div>

            {/* 结果内容 */}
            <div className="flex-1 overflow-auto">
              {results.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-center px-4">
                  <Activity className="w-10 h-10 text-[#c7c7c7] mb-3" />
                  <p className="text-[15px] font-medium text-[#1d1d1f] mb-1">暂无结果</p>
                  <p className="text-[13px] text-[#8e8e8e]">输入目标地址并点击开始探测</p>
                </div>
              ) : (
                <table className="w-full">
                  <thead className="bg-[#fafafa] sticky top-0 border-b border-[#d1d1d6]">
                    <tr>
                      <th className="px-4 py-2 text-left text-[11px] font-semibold text-[#8e8e8e] uppercase tracking-wide w-12">
                        #
                      </th>
                      <th className="px-4 py-2 text-left text-[11px] font-semibold text-[#8e8e8e] uppercase tracking-wide">
                        地址
                      </th>
                      <th className="px-4 py-2 text-left text-[11px] font-semibold text-[#8e8e8e] uppercase tracking-wide w-20">
                        状态
                      </th>
                      <th className="px-4 py-2 text-left text-[11px] font-semibold text-[#8e8e8e] uppercase tracking-wide">
                        用户名
                      </th>
                      <th className="px-4 py-2 text-left text-[11px] font-semibold text-[#8e8e8e] uppercase tracking-wide">
                        密码
                      </th>
                      <th className="px-4 py-2 text-left text-[11px] font-semibold text-[#8e8e8e] uppercase tracking-wide">
                        详情
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#e5e5e5]">
                    {results.map((result) => (
                      <tr key={result.id} className="hover:bg-[#f5f5f7] transition-colors">
                        <td className="px-4 py-2.5 text-[13px] text-[#8e8e8e] tabular-nums">{result.id}</td>
                        <td className="px-4 py-2.5 text-[13px] text-[#1d1d1f] font-mono">{result.address}</td>
                        <td className="px-4 py-2.5">
                          <div className="flex items-center gap-1.5">
                            {getStatusIcon(result.status)}
                            <span className="text-[13px] text-[#1d1d1f]">{getStatusText(result.status)}</span>
                          </div>
                        </td>
                        <td className="px-4 py-2.5 text-[13px] text-[#1d1d1f] font-mono">{result.username}</td>
                        <td className="px-4 py-2.5 text-[13px] text-[#1d1d1f] font-mono">{result.password}</td>
                        <td className="px-4 py-2.5 text-[13px] text-[#8e8e8e]">{result.details}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
