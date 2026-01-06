# OpenWrt Manager - 浏览器插件版技术方案

**项目代号**: OM Extension  
**类型**: Chrome Extension (Manifest V3)  
**定位**: 轻量级、伴随式 OpenWrt 管理助手

---

## 1. 核心差异 (vs 桌面版)

| 特性 | 桌面版 (现有) | 插件版 (新开) |
| :--- | :--- | :--- |
| **通信协议** | SSH (TCP 22) + HTTP | **HTTP (uBus JSON-RPC)** Only |
| **核心能力** | 终端管理、高级配置、刷机 | **状态监控、开关控制、页面增强** |
| **网络权限** | 操作系统级网络栈 | **Host Permissions (绕过 CORS)** |
| **存储** | 本地文件系统 (SQLite/JSON) | **chrome.storage.local** |

---

## 2. 技术选型

### A. 开发框架: WXT (Next-gen Framework)
我们推荐使用 **WXT** (wxt.dev) 而不是裸写 Webpack。
- **理由**: 它像 Nuxt/Next.js 一样开箱即用，支持 React HMR，自动处理 Manifest，体验极佳。
- **语言**: TypeScript

### B. UI 框架: React + Tailwind CSS
- **复用**: 复用桌面版的 UI 设计语言 (Glassmorphism)。
- **组件库**: Radix UI (保持一致性)。

### C. 通信层: uBus Client
- **废弃**: `paramiko` (Python SSH)
- **新建**: `uBusClient.ts`
  - 使用 `fetch()` 直接请求路由器的 `/ubus` 接口。
  - 需要处理 Session ID (Auth Token) 的获取和保活。

---

## 3. 功能规划 (MVP)

1.  **Popup (点击图标弹出)**
    -   显示当前路由器 CPU / 内存 / 温度。
    -   显示实时上传/下载速率。
    -   快速开关 (重启 WiFi、重启路由)。

2.  **Options (设置页)**
    -   配置路由器地址 (如 `192.168.1.1`)。
    -   配置用户名/密码 (保存到 encrypted storage)。

3.  **Content Script (LuCI 注入)** [P2优先级]
    -   自动检测 LuCI 登录页，提供"一键填充"功能。
    -   美化 LuCI 界面 CSS。
