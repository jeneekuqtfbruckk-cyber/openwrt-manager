# AI 辅助开发策略：主从同步模式 (Master-Replica Pattern)

**背景**: 在 AI 主导开发的多项目环境 (One User, Multiple AIs) 中，传统的 "Shared Library" 会因为 AI 上下文隔离而导致维护灾难。

**核心理念**: **Single Source of Truth (单一事实来源)**。
我们不要求两个 AI 协商共识，而是定义一个"主"，另一个为"从"。

---

## 1. 角色定义

| 项目 | 角色 | 权限 | AI 指令 |
| :--- | :--- | :--- | :--- |
| **Desktop App** | **Master (主)** | ✅ **读写** UI 定义 | "你可以随意修改 globals.css 和组件设计，这是你的地盘。" |
| **Extension** | **Replica (从)** | 🚫 **只读** UI 定义 | "严禁修改 globals.css 和 ui/ 目录。如果你需要改样式，请告诉用户去 Desktop 项目改。" |

## 2. 同步机制 (The Bridge)

我们不通过复杂的 npm link 或 git submodule 来同步，而是用一个简单暴力的 **Python 脚本 (`sync-ui.py`)**。

**工作流**:
1.  您在 **Desktop 对话窗** 让 AI 修改了 UI（比如把按钮变圆）。
2.  您在终端运行 `python sync-ui.py`。
3.  脚本自动把 Desktop 的 CSS 和组件**强制覆盖**到 Extension 目录。
4.  您切换到 **Extension 对话窗**，AI 发现文件变了，直接使用新样式。

## 3. 优势

1.  **零脑力负担**: 您不需要记着"改了A要改B"，脚本替您记。
2.  **避免 AI 打架**: Extension AI 绝不会自作主张去改 UI 导致两边不一致。
3.  **上下文解耦**: Extension AI 甚至不需要知道 Desktop 的存在，它只看到它的目录下有现成的 UI 文件可以用。

---

## 4. 目录结构

```text
E:\xcode\openwrt-manager\
├── open-wrt-manager-ui (2)\  <-- [Master] UI 源头
├── browser-extension\        <-- [Replica] UI 副本
└── sync-ui.py                <-- [Bridge] 同步脚本
```
