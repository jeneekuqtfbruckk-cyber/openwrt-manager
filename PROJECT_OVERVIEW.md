# OpenWrt Manager - 项目全览

> **一站式掌握整个项目** - 面向开发者的完整技术文档

---

## 📋 项目基本信息

| 项目属性 | 信息 |
|---------|------|
| **项目名称** | OpenWrt Manager |
| **项目类型** | 桌面应用（Electron + Python） |
| **当前版本** | v2.0.1 |
| **开源协议** | MIT License |
| **GitHub仓库** | [jeneekuqtfbruckk-cyber/openwrt-manager](https://github.com/jeneekuqtfbruckk-cyber/openwrt-manager) |
| **主要语言** | TypeScript, Python, JavaScript |
| **目标平台** | Windows (x64) |
| **开发周期** | 2025-12 ~ 2026-01 |

---

## 🎯 项目定位

### 核心功能
批量管理多台 OpenWrt 路由器的桌面工具：
- 🔍 自动发现局域网内的 OpenWrt 设备
- 🔐 批量登录管理（SSH/HTTP）
- 📊 实时状态监控
- ⚙️ 配置批量同步

### 技术特色
- **Mac 风格 UI** - 现代化的视觉设计（Glassmorphism）
- **Electron + Python 混合架构** - Web 技术 + 系统能力
- **一键式安装** - NSIS 辅助安装向导
- **开箱即用** - 无需额外依赖

---

## 🏗️ 技术架构

### 架构图

```
┌─────────────────────────────────────────────────┐
│         Electron 主进程                          │
│  ┌──────────────┐        ┌──────────────┐      │
│  │ 窗口管理     │        │ 进程管理     │      │
│  │ IPC 通信     │        │ 后端启动     │      │
│  └──────────────┘        └──────────────┘      │
└─────────────────────────────────────────────────┘
         ▲                         ▲
         │ IPC                     │ 子进程
         ▼                         ▼
┌─────────────────┐       ┌─────────────────┐
│  Renderer 进程   │       │  Python Backend │
│  (Next.js UI)   │◄─────►│   (FastAPI)     │
│                 │ HTTP  │                 │
│  - React 19     │       │  - SSH 客户端   │
│  - Tailwind CSS │       │  - 路由器扫描   │
│  - Radix UI     │       │  - 状态查询     │
└─────────────────┘       └─────────────────┘
```

### 技术栈详解

#### 前端层
```yaml
框架: Next.js 16 (App Router)
UI库: React 19
样式: Tailwind CSS + 自定义设计系统
组件: Radix UI (无样式组件基础)
状态管理: React Hooks
HTTP客户端: fetch API
```

#### 桌面层
```yaml
框架: Electron 28
主进程: 窗口管理、菜单、托盘、IPC
渲染进程: Next.js 应用
打包: electron-builder
安装: NSIS (辅助模式)
```

#### 后端层
```yaml
框架: FastAPI (异步)
ASGI服务器: Uvicorn
SSH库: paramiko
打包: PyInstaller (单文件EXE)
启动模式: 子进程（by Electron）
```

---

## 📁 目录结构

```
openwrt-manager/
├── .github/                    # GitHub配置
│   └── workflows/
│       └── build-release.yml   # CI/CD自动构建
│
├── .internal/                  # 内部文档（不上传Git）
│   ├── ai-assistance/          # AI对话记录
│   ├── archive/                # 历史归档（旧版本、构建日志）
│   ├── experiments/            # 技术实验（Flet等）
│   ├── knowledge-base/         # 📚 知识库 ⭐
│   │   ├── tools-and-websites.md
│   │   ├── electron-development.md
│   │   ├── github-actions-ci-cd.md
│   │   ├── first-run-backend-delay.md
│   │   └── signpath-free-signing.md
│   ├── planning/               # 项目计划
│   ├── retrospectives/         # 项目复盘
│   └── temp/                   # 临时文件（已清空）
│
├── backend/                    # Python后端 🐍
│   ├── main.py                 # FastAPI入口
│   ├── scanner.py              # 路由器扫描逻辑
│   ├── backend.spec            # PyInstaller配置
│   ├── requirements.txt        # Python依赖
│   └── run_server.bat          # 本地测试脚本
│
├── build/                      # 构建资源
│   ├── icon.ico                # 应用图标（多分辨率）
│   └── icon-source.png         # 图标源文件
│
├── favicon_io/                 # 图标设计文件
│
├── open-wrt-manager-ui (2)/    # 前端 + Electron ⚡
│   ├── app/                    # Next.js App Router
│   │   ├── globals.css         # 全局样式
│   │   ├── layout.tsx          # 根布局
│   │   └── page.tsx            # 首页
│   ├── components/             # React组件
│   │   ├── openwrt-manager.tsx # 主组件
│   │   └── ui/                 # Radix UI组件
│   ├── public/                 # 静态资源
│   │   └── icon.ico            # 打包用图标
│   ├── main.js                 # Electron主进程
│   ├── renderer.js             # Electron渲染进程
│   ├── next.config.mjs         # Next.js配置
│   ├── package.json            # 项目配置⭐
│   └── tailwind.config.ts      # Tailwind配置
│
├── screenshots/                # 应用截图
│   └── app-interface.png       # 界面截图
│
├── scripts/                    # 工具脚本
│   ├── release.js              # 自动发布脚本
│   └── utils/                  # 工具集（Git同步等）
│
├── .gitignore                  # Git忽略规则
├── LICENSE.txt                 # MIT许可证
├── PROJECT_OVERVIEW.md         # 📖 本文件 ⭐
└── README.md                   # GitHub说明文档
```

---

## 🚀 开发流程

### 1. 本地开发环境

```bash
# 前提条件
- Node.js 20+
- Python 3.11
- Git

# 克隆仓库
git clone https://github.com/jeneekuqtfbruckk-cyber/openwrt-manager.git
cd openwrt-manager

# 安装前端依赖
cd "open-wrt-manager-ui (2)"
npm install

# 安装后端依赖
cd ../backend
pip install -r requirements.txt

# 启动开发服务器
npm run dev              # 前端 (Next.js)
python backend/main.py   # 后端 (FastAPI)
```

### 2. 打包流程

```bash
# 本地打包（需要完整构建环境）
npm run package          # 前端 + Electron
npm run build:backend    # 后端 (PyInstaller)

# 输出
dist/OpenWrt-Manager-Setup-2.0.1.exe  # NSIS安装包
```

### 3. 发布流程

```bash
# 使用自动化脚本
node scripts/release.js

# 输入版本号（如 v2.0.2）
# 自动执行：
#  - git add .
#  - git commit
#  - git push
#  - git tag -f v2.0.2
#  - git push origin v2.0.2 -f
#  - 触发 GitHub Actions 自动构建
```

### 4. CI/CD 自动化

**触发条件**: 推送 tag `v*`  
**运行平台**: GitHub Actions (windows-latest)  
**构建时间**: ~10-15 分钟  
**输出**: GitHub Release + 安装包

**工作流步骤**:
1. 检出代码
2. 设置 Python 3.11
3. 设置 Node.js 20
4. 构建后端 (PyInstaller)
5. 安装前端依赖
6. 构建前端 (Next.js)
7. 复制图标文件
8. 打包 Electron 应用 (NSIS)
9. 创建 GitHub Release
10. 上传安装包

---

## 🔑 关键技术点

### 1. Electron + Python 通信

**启动流程**:
```javascript
// main.js - Electron主进程
const backendProcess = spawn('backend.exe', [], {
  cwd: resourcesPath,
  detached: false
});

// 等待后端就绪（3-5秒）
await waitForBackend('http://127.0.0.1:8000/health');

// 创建窗口并加载前端
mainWindow.loadURL('http://localhost:3000');
```

**通信方式**:
- 前端 → 后端: HTTP API (`fetch`)
- 前端 ↔ Electron: IPC (`ipcRenderer`/`ipcMain`)

### 2. Mac 风格 UI 实现

```css
/* globals.css - 毛玻璃效果 */
.glassmorphism {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
}

/* 微动画 */
.hover-lift {
  transition: all 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}
```

### 3. NSIS 辅助安装

**配置亮点** (package.json):
```json
{
  "nsis": {
    "oneClick": false,              // 辅助模式（非静默）
    "allowToChangeInstallationDirectory": true,
    "license": "../LICENSE.txt",
    "createDesktopShortcut": "always",
    "displayLanguageSelector": true,
    "installerLanguages": ["zh_CN", "en_US"],
    "perMachine": true              // 所有用户可用
  }
}
```

### 4. 首次启动延迟问题

**问题**: 第一次扫描全部失败  
**原因**: FastAPI 后端启动需要 3-5 秒  
**解决**: `waitForBackend()` 函数确保后端就绪再显示窗口

---

## 📦 打包说明

### 最终产物

```
OpenWrt-Manager-Setup-2.0.1.exe
├── [嵌入资源]
│   ├── Next.js 前端（已构建）
│   ├── Electron 运行时
│   ├── backend.exe (PyInstaller单文件)
│   │   ├── Python 3.11解释器
│   │   ├── FastAPI框架
│   │   ├── paramiko库
│   │   └── 所有依赖
│   └── 图标资源
└── [安装逻辑]
    ├── 用户许可协议
    ├── 安装路径选择
    ├── 快捷方式创建
    └── 注册表注册
```

### 大小分析

- **安装包**: ~120 MB
- **安装后**: ~180 MB
  - Electron 运行时: ~100 MB
  - backend.exe: ~15 MB
  - Next.js 静态文件: ~50 MB
  - 图标和资源: ~15 MB

---

## 🔐 代码签名 (SignPath)

### 当前状态

**配置完成度**: ✅ 100%  
**审核状态**: ⏳ 等待人工审核（1-2周）

**已完成配置**:
- ✅ Organization: `openwrt-manager`
- ✅ Project: `OpenWrt Manager`
- ✅ Artifact Configuration: `Release Installer`
- ✅ Signing Policy: `Release Builds`
- ✅ Test Certificate: `Test Certificate`
- ✅ CI User: `GitHub Actions`
- ✅ API Token: `AP/IHzc2...` (已生成)

**待办事项**:
1. 添加 `SIGNPATH_API_TOKEN` 到 GitHub Secrets
2. 安装 SignPath GitHub App
3. 等待开源项目审核通过
4. 更新 workflow 添加签名步骤

### 签名后效果

- ✅ 移除 Windows SmartScreen 警告
- ✅ 移除 360 安全卫士拦截
- ✅ 显示 "SignPath Foundation" 证书
- ✅ 提升用户信任度

---

## 🐛 已知问题与解决

### 1. 首次测试失败
**问题**: 用户报告第一次扫描全部失败  
**原因**: 后端启动需要 3-5 秒  
**状态**: ✅ 已解释（正常现象）  
**文档**: `.internal/knowledge-base/first-run-backend-delay.md`

### 2. 图标缓存问题
**问题**: 更新图标后不显示  
**原因**: Windows 图标缓存  
**解决**: 重启系统或清理缓存  
**状态**: ✅ 已解决

### 3. 杀毒软件误报
**问题**: 360/腾讯管家报毒  
**原因**: 未签名的 EXE  
**解决**: SignPath 免费代码签名  
**状态**: ⏳ 配置完成，等待审核

---

## 📚 知识库索引

项目积累的技术文档（位于 `.internal/knowledge-base/`）:

| 文档 | 主题 | 关键内容 |
|------|------|----------|
| **tools-and-websites.md** | 开发工具清单 | 所有使用的软件、网站、AI工具 |
| **electron-development.md** | Electron开发经验 | 混合架构、Mac风格UI、打包策略 |
| **github-actions-ci-cd.md** | CI/CD经验 | 6大常见问题、Workflow模板 |
| **first-run-backend-delay.md** | 启动延迟问题 | 3-5秒初始化原因和解决方案 |
| **signpath-free-signing.md** | 免费签名配置 | SignPath申请、配置、审核流程 |

---

## 🎯 未来规划

### 短期（1个月内）
- [ ] SignPath 审核通过，启用免费签名
- [ ] 添加自动更新功能
- [ ] 优化首次启动体验
- [ ] 增加详细的错误提示

### 中期（3个月内）
- [ ] 开发 Web 版本（纯浏览器访问）
- [ ] 支持 Mac/Linux 平台
- [ ] 增加路由器配置备份功能
- [ ] 实现批量脚本执行

### 长期（6个月+）
- [ ] 插件系统（用户自定义功能）
- [ ] 团队协作功能
- [ ] 数据可视化仪表盘
- [ ] 移动端配套 App

---

## 🤝 贡献指南

### 提交 PR 流程
1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范
- TypeScript: ESLint + Prettier
- Python: PEP 8 + Black
- Commit: Conventional Commits

---

## 📞 联系方式

- **GitHub Issues**: [提交问题](https://github.com/jeneekuqtfbruckk-cyber/openwrt-manager/issues)
- **Discussions**: [讨论区](https://github.com/jeneekuqtfbruckk-cyber/openwrt-manager/discussions)
- **Email**: (项目维护者邮箱)

---

## 📄 许可证

本项目采用 MIT License 开源协议。

详见 [LICENSE.txt](LICENSE.txt)

---

**文档版本**: v1.0  
**最后更新**: 2026-01-04  
**维护者**: OpenWrt Manager Team
