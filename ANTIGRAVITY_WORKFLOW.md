# Antigravity 混合架构编排手册 (Orchestration Manual)

基于 **Antigravity + Gemini 3 Pro** 的 "Dual-Track Agent" 开发模式指南。

## 核心理念
我们不再在一个聊天流中混杂所有指令，而是利用 Antigravity 的 **Manager View** 启动并行的、上下文隔离的 Agent 实例。

---

## 🚀 启动流程 (Workflow)

### 1. 启动 Desktop Agent (Track A)
*   **操作**: 在 Manager View 点击 "New Session"
*   **Target Directory**: `E:\xcode\openwrt-manager\open-wrt-manager-ui (2)`
*   **Prompt**: "启动开发模式。请遵循当前目录下的 `AGENTS.md`。"
*   **作用**: 这个 Agent 将瞬间精通 Electron/Python，而完全不知道插件的存在。

### 2. 启动 Extension Agent (Track B)
*   **操作**: 在 Manager View 点击 "New Session" (第二个)
*   **Target Directory**: `E:\xcode\openwrt-manager\browser-extension`
*   **Prompt**: "启动开发模式。请遵循 `AGENTS.md`。初始化 WXT 项目。"
*   **作用**: 这个 Agent 将被物理锁定在插件目录下。它看到的 `AGENTS.md` 会告诉它："你只有 Chrome API 权限"。

---

## 🧩 协作模式 (Collaboration)

当需要 UI 同步时（例如：把 Desktop 的 Glassmorphism 样式同步给 Extension）：

1.  **User**: 打开 **Track B (Extension Agent)** 的窗口。
2.  **User**: "请读取 `../open-wrt-manager-ui (2)/open-wrt-manager-ui (2)/app/globals.css` 作为参考，配置我的 Tailwind v4。"
3.  **Agent B**: 因为它的 `AGENTS.md` 允许“读取参考”但禁止“写回”，它会安全地把样式搬运过来。

---

## 🛡️ 制品门禁 (Artifact Gate)

在 Planning Mode 下：
*   **Desktop Agent** 生成的计划书必须包含：IPC 定义、Python 路由、Electron Builder 配置。
*   **Extension Agent** 生成的计划书必须包含：Manifest V3 权限、Message Passing、WXT 构建流。
*   **审查点**: 如果 Extension Agent 的计划里出现了 "Run Python Script"，直接打回重写。

---

## 📂 目录映射

| 概念名称 | 实际目录 | 规则文件 |
| :--- | :--- | :--- |
| **App Root** | `open-wrt-manager-ui (2)` | `AGENTS.md` (Electron/Python) |
| **Ext Root** | `browser-extension` | `AGENTS.md` (WXT/React) |
