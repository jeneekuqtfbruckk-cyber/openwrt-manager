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
  const [showThreadsMenu, setShowThreadsMenu] = useState(false)
  const [isScanning, setIsScanning] = useState(false)
  const [results, setResults] = useState<ScanResult[]>([])
  const [showExportMenu, setShowExportMenu] = useState(false)
  const [activeMenu, setActiveMenu] = useState<string | null>(null)

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

  const menuItems = [
    {
      label: "OpenWrt Manager",
      bold: true,
      items: [
        { label: "关于 OpenWrt Manager", shortcut: "" },
        { divider: true },
        { label: "偏好设置...", shortcut: "⌘," },
        { divider: true },
        { label: "隐藏 OpenWrt Manager", shortcut: "⌘H" },
        { label: "隐藏其他", shortcut: "⌥⌘H" },
        { label: "显示全部", shortcut: "" },
        { divider: true },
        { label: "退出 OpenWrt Manager", shortcut: "⌘Q" },
      ],
    },
    {
      label: "文件",
      items: [
        { label: "新建窗口", shortcut: "⌘N" },
        { label: "打开...", shortcut: "⌘O" },
        { divider: true },
        { label: "导入目标列表...", shortcut: "⌘I" },
        { label: "导出结果...", shortcut: "⌘E" },
        { divider: true },
        { label: "关闭窗口", shortcut: "⌘W" },
      ],
    },
    {
      label: "编辑",
      items: [
        { label: "撤销", shortcut: "⌘Z" },
        { label: "重做", shortcut: "⇧⌘Z" },
        { divider: true },
        { label: "剪切", shortcut: "⌘X" },
        { label: "拷贝", shortcut: "⌘C" },
        { label: "粘贴", shortcut: "⌘V" },
        { label: "全选", shortcut: "⌘A" },
      ],
    },
    {
      label: "视图",
      items: [
        { label: "显示侧边栏", shortcut: "⌘S", checked: true },
        { label: "显示概览", shortcut: "⌘O", checked: true },
        { divider: true },
        { label: "放大", shortcut: "⌘+" },
        { label: "缩小", shortcut: "⌘-" },
        { label: "实际大小", shortcut: "⌘0" },
        { divider: true },
        { label: "进入全屏幕", shortcut: "⌃⌘F" },
      ],
    },
    {
      label: "扫描",
      items: [
        { label: "开始扫描", shortcut: "⌘R" },
        { label: "停止扫描", shortcut: "⌘." },
        { divider: true },
        { label: "清除结果", shortcut: "⌘K" },
      ],
    },
    {
      label: "窗口",
      items: [
        { label: "最小化", shortcut: "⌘M" },
        { label: "缩放", shortcut: "" },
        { divider: true },
        { label: "将所有窗口置于前面", shortcut: "" },
      ],
    },
    {
      label: "帮助",
      items: [
        { label: "OpenWrt Manager 帮助", shortcut: "" },
        { divider: true },
        { label: "查看文档", shortcut: "" },
        { label: "报告问题...", shortcut: "" },
      ],
    },
  ]

  const threadOptions = [50, 100, 200]

  return (
    <div className="w-full max-w-[1200px]">
      {activeMenu && <div className="fixed inset-0 z-40" onClick={() => setActiveMenu(null)} />}
      {(showThreadsMenu || showExportMenu) && (
        <div
          className="fixed inset-0 z-30"
          onClick={() => {
            setShowThreadsMenu(false)
            setShowExportMenu(false)
          }}
        />
      )}

      <div className="bg-[#f5f5f7] rounded-[10px] shadow-2xl overflow-hidden border border-[#c7c7c7]">
        <div className="h-[52px] bg-gradient-to-b from-[#e8e8e8] to-[#d4d4d4] border-b border-[#b8b8b8] flex items-center px-4 relative">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-[#ff5f57] border border-[#e0443e] hover:brightness-90 cursor-pointer" />
            <div className="w-3 h-3 rounded-full bg-[#febc2e] border border-[#d4a528] hover:brightness-90 cursor-pointer" />
            <div className="w-3 h-3 rounded-full bg-[#28c840] border border-[#24a732] hover:brightness-90 cursor-pointer" />
          </div>
          <div className="absolute left-1/2 -translate-x-1/2 flex items-center gap-2">
            <span className="text-[13px] font-medium text-[#4d4d4d]">OpenWrt Manager</span>
            <span className="text-[11px] text-[#8e8e8e]">v2.0</span>
          </div>
        </div>

        <div className="h-7 bg-gradient-to-b from-[#f5f5f5] to-[#e8e8e8] border-b border-[#c7c7c7] flex items-center px-3 relative z-50">
          <div className="flex items-center">
            {menuItems.map((menu) => (
              <div key={menu.label} className="relative">
                <button
                  className={`px-2.5 py-0.5 text-[13px] rounded transition-colors ${menu.bold ? "font-semibold" : ""} ${
                    activeMenu === menu.label ? "bg-[#0061d5] text-white" : "text-[#1d1d1f] hover:bg-black/5"
                  }`}
                  onClick={() => setActiveMenu(activeMenu === menu.label ? null : menu.label)}
                >
                  {menu.label}
                </button>

                {activeMenu === menu.label && (
                  <div className="absolute top-full left-0 mt-0.5 min-w-[220px] bg-[#f6f6f6]/95 backdrop-blur-xl rounded-md shadow-xl border border-[#c7c7c7]/50 py-1 z-50">
                    {menu.items.map((item, idx) =>
                      item.divider ? (
                        <div key={idx} className="h-px bg-[#d1d1d6] my-1 mx-2" />
                      ) : (
                        <button
                          key={idx}
                          className="w-full px-3 py-1 text-[13px] text-[#1d1d1f] hover:bg-[#0061d5] hover:text-white text-left flex items-center justify-between group"
                        >
                          <span className="flex items-center gap-2">
                            {item.checked && <span className="text-[12px]">✓</span>}
                            {item.label}
                          </span>
                          {item.shortcut && (
                            <span className="text-[12px] text-[#8e8e8e] group-hover:text-white/70 ml-4">
                              {item.shortcut}
                            </span>
                          )}
                        </button>
                      ),
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className="ml-auto flex items-center gap-3">
            {isScanning && (
              <div className="flex items-center gap-1.5">
                <div className="w-2 h-2 bg-[#34c759] rounded-full animate-pulse" />
                <span className="text-[12px] text-[#1d1d1f]">扫描中</span>
              </div>
            )}
            <span className="text-[12px] text-[#1d1d1f]">
              {new Date().toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" })}
            </span>
          </div>
        </div>

        <div className="flex" style={{ height: "calc(100vh - 180px)", minHeight: "500px" }}>
          <div className="w-[280px] bg-[#f5f5f7] border-r border-[#d1d1d6] flex flex-col">
            <div className="p-4 flex-1 flex flex-col">
              <h2 className="text-[11px] font-semibold text-[#8e8e8e] uppercase tracking-wide mb-2">目标</h2>
              <textarea
                value={targets}
                onChange={(e) => setTargets(e.target.value)}
                placeholder="输入 IP 地址，每行一个..."
                className="w-full flex-1 min-h-[200px] px-3 py-2 text-[13px] text-[#1d1d1f] placeholder:text-[#8e8e8e] bg-white rounded-[6px] border border-[#c7c7c7] focus:outline-none focus:border-[#0071e3] focus:ring-2 focus:ring-[#0071e3]/20 resize-none leading-relaxed"
              />
            </div>

            <div className="p-4 pt-0">
              <div className="flex items-center gap-2">
                <div className="relative">
                  <button
                    onClick={() => setShowThreadsMenu(!showThreadsMenu)}
                    className="h-10 px-3 bg-white hover:bg-[#fafafa] border border-[#c7c7c7] text-[#1d1d1f] text-[13px] rounded-[6px] transition-all duration-150 flex items-center gap-2 active:scale-[0.98]"
                  >
                    <span className="text-[#8e8e8e]">并发</span>
                    <span className="font-medium tabular-nums">{threads}</span>
                    <ChevronDown
                      className={`w-3.5 h-3.5 text-[#8e8e8e] transition-transform duration-150 ${showThreadsMenu ? "rotate-180" : ""}`}
                    />
                  </button>
                  {showThreadsMenu && (
                    <div className="absolute bottom-full left-0 mb-1 bg-white rounded-[6px] shadow-lg border border-[#c7c7c7] overflow-hidden z-40">
                      {threadOptions.map((option) => (
                        <button
                          key={option}
                          onClick={() => {
                            setThreads(option)
                            setShowThreadsMenu(false)
                          }}
                          className={`w-full px-4 py-2 text-[13px] text-left transition-colors flex items-center justify-between gap-4 ${
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
                  className="flex-1 h-10 bg-[#0071e3] hover:bg-[#0077ed] disabled:bg-[#8e8e8e] text-white text-[13px] font-medium rounded-[6px] transition-all duration-150 flex items-center justify-center gap-2 disabled:cursor-not-allowed active:scale-[0.98]"
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
              </div>
            </div>

            <div className="p-4 border-t border-[#d1d1d6]">
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
            <div className="h-10 bg-[#fafafa] border-b border-[#d1d1d6] flex items-center justify-between px-4">
              <div className="flex items-center">
                <h2 className="text-[11px] font-semibold text-[#8e8e8e] uppercase tracking-wide">结果</h2>
                {results.length > 0 && <span className="ml-2 text-[11px] text-[#8e8e8e]">({results.length})</span>}
              </div>
              <div className="relative">
                <button
                  onClick={() => setShowExportMenu(!showExportMenu)}
                  className="h-7 px-2.5 bg-white hover:bg-[#f5f5f7] border border-[#c7c7c7] text-[#1d1d1f] text-[12px] rounded-[5px] transition-all duration-150 flex items-center gap-1.5 active:scale-[0.98]"
                >
                  <Download className="w-3 h-3" />
                  <span>导出</span>
                  <ChevronDown
                    className={`w-3 h-3 transition-transform duration-150 ${showExportMenu ? "rotate-180" : ""}`}
                  />
                </button>
                {showExportMenu && (
                  <div className="absolute top-full right-0 mt-1 bg-white rounded-[6px] shadow-lg border border-[#c7c7c7] overflow-hidden z-40 min-w-[120px]">
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
