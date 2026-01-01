# 测试说明

## 本地测试环境准备

### 方法 1: 使用本地 OpenWrt 虚拟机（推荐）

如果你有 OpenWrt 虚拟机，可以直接测试：

1. 确保虚拟机网络配置正确
2. 记录虚拟机的 IP 地址（例如 `192.168.1.1`）
3. 在程序中输入该 IP 进行测试

### 方法 2: 使用测试服务器模拟（开发测试）

创建一个简单的 Flask 服务器来模拟 OpenWrt LuCI 登录行为。

#### 测试服务器代码（test_server.py）

```python
from flask import Flask, request, make_response, redirect

app = Flask(__name__)

# 模拟的有效凭证
VALID_CREDENTIALS = {
    "root": "password"
}

@app.route('/cgi-bin/luci', methods=['GET', 'POST'])
def luci_login():
    if request.method == 'POST':
        username = request.form.get('luci_username')
        password = request.form.get('luci_password')
        
        print(f"[测试服务器] 收到登录请求: {username} / {password}")
        
        # 检查凭证
        if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
            print(f"[测试服务器] ✅ 登录成功")
            # 模拟成功 - 返回 302 并设置 sysauth Cookie
            response = make_response(redirect('/'))
            response.set_cookie('sysauth', 'test_token_12345')
            return response
        else:
            print(f"[测试服务器] ❌ 登录失败")
            # 模拟失败 - 返回 403
            return "Login failed", 403
    
    return "OpenWrt Login Test Server", 200

if __name__ == '__main__':
    print("🚀 启动测试服务器...")
    print("📍 访问地址: http://127.0.0.1:5000")
    print("✅ 有效凭证: root / password")
    app.run(host='0.0.0.0', port=5000, debug=True)
```

#### 运行测试服务器

1. 安装 Flask:
   ```bash
   pip install flask
   ```

2. 运行服务器:
   ```bash
   python test_server.py
   ```

3. 在 OpenWrt 管理助手中输入:
   ```
   http://127.0.0.1:5000
   ```

---

## 功能测试清单

### ✅ UI 界面测试

- [ ] 主窗口正常显示
- [ ] 左右分栏比例正确（30% / 70%）
- [ ] URL 输入框有 placeholder 提示
- [ ] 并发数调整框默认值为 50
- [ ] 开始按钮显示绿色
- [ ] 呼吸灯显示灰色
- [ ] 表格列标题正确显示

### ✅ 基本功能测试

- [ ] 输入单个 URL 并探测
- [ ] 输入多个 URL 并探测
- [ ] 点击"停止"按钮能中断探测
- [ ] 调整并发数后生效
- [ ] 探测完成后显示完成提示

### ✅ 呼吸灯动画测试

- [ ] 探测前：灰色静止
- [ ] 探测中：绿色呼吸闪烁
- [ ] 探测后：恢复灰色静止

### ✅ 表格颜色标记测试

- [ ] 登录成功：浅绿色背景
- [ ] 登录失败：浅红色背景
- [ ] 连接超时：浅红色背景
- [ ] 无法连接：浅红色背景

### ✅ 异步性能测试

- [ ] 探测 10 个目标时界面不卡顿
- [ ] 探测 50 个目标时界面不卡顿
- [ ] 探测 100 个目标时界面不卡顿
- [ ] 统计信息实时更新

### ✅ CSV 导出测试

- [ ] 导出按钮在探测前禁用
- [ ] 导出按钮在探测后启用
- [ ] 导出的 CSV 文件包含正确的列
- [ ] 导出的 CSV 文件可以用 Excel 打开
- [ ] 中文内容无乱码

### ✅ 异常处理测试

- [ ] 输入无效 IP 地址（如 `999.999.999.999`）
- [ ] 输入不存在的域名（如 `http://nonexistent.example`）
- [ ] 网络断开时的行为
- [ ] 目标设备关机时的行为

---

## 性能测试

### 并发测试

测试不同并发数下的性能：

| 并发数 | 目标数量 | 实际耗时 | UI 是否流畅 | 备注 |
|--------|----------|----------|-------------|------|
| 10     | 50       |          | ✅ / ❌      |      |
| 50     | 100      |          | ✅ / ❌      |      |
| 100    | 200      |          | ✅ / ❌      |      |
| 200    | 500      |          | ✅ / ❌      |      |

### 大规模测试

- [ ] 测试 500 个目标
- [ ] 测试 1000 个目标
- [ ] 记录内存占用情况
- [ ] 记录 CPU 占用情况

---

## 已知限制

1. **CSRF Token**: 某些新版 OpenWrt 可能需要先获取 CSRF Token，当前版本会标记"需 Token"但不会自动处理
2. **HTTPS 证书**: 忽略了 SSL 证书验证，仅适用于内网环境
3. **并发限制**: 虽然支持最高 500 并发，但实际受限于系统资源

---

## 下一步优化方向

1. 支持自定义登录路径
2. 支持 CSRF Token 自动获取
3. 支持多种登录协议（SSH、Telnet 等）
4. 支持从文件导入目标列表
5. 支持定时任务和自动探测
6. 支持结果过滤和搜索

---

## 测试报告模板

```
测试时间: ________
测试人员: ________

环境信息:
- 操作系统: ________
- Python 版本: ________
- 依赖库版本: ________

测试结果:
- UI 界面: ✅ / ❌
- 基本功能: ✅ / ❌
- 呼吸灯动画: ✅ / ❌
- 颜色标记: ✅ / ❌
- 异步性能: ✅ / ❌
- CSV 导出: ✅ / ❌
- 异常处理: ✅ / ❌

发现的问题:
1. ________
2. ________

建议改进:
1. ________
2. ________
```
