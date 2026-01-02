"""
OpenWrt LuCI 登录测试服务器
用于本地测试 OpenWrt 批量资产管理助手
"""

from flask import Flask, request, make_response, redirect

app = Flask(__name__)

# 模拟的有效凭证
VALID_CREDENTIALS = {
    "root": "password",
    "admin": "admin"
}

@app.route('/cgi-bin/luci', methods=['GET', 'POST'])
def luci_login():
    """模拟 OpenWrt LuCI 登录接口"""
    if request.method == 'POST':
        username = request.form.get('luci_username')
        password = request.form.get('luci_password')
        
        print(f"[测试服务器] 收到登录请求: {username} / {password}")
        
        # 检查凭证
        if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
            print(f"[测试服务器] ✅ 登录成功: {username}")
            # 模拟成功 - 返回 302 并设置 sysauth Cookie
            response = make_response(redirect('/'))
            response.set_cookie('sysauth', f'test_token_{username}_12345')
            return response
        else:
            print(f"[测试服务器] ❌ 登录失败: {username} / {password}")
            # 模拟失败 - 返回 403
            return "Login failed", 403
    
    return """
    <html>
    <head><title>OpenWrt LuCI Test Server</title></head>
    <body>
        <h1>OpenWrt LuCI 测试服务器</h1>
        <p>有效凭证:</p>
        <ul>
            <li>root / password</li>
            <li>admin / admin</li>
        </ul>
    </body>
    </html>
    """, 200

@app.route('/')
def index():
    """登录成功后的页面"""
    return """
    <html>
    <head><title>OpenWrt Dashboard</title></head>
    <body>
        <h1>✅ 登录成功</h1>
        <p>欢迎来到 OpenWrt 管理界面（测试）</p>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 启动 OpenWrt LuCI 测试服务器...")
    print("=" * 60)
    print("📍 访问地址: http://127.0.0.1:5000")
    print("📍 登录接口: http://127.0.0.1:5000/cgi-bin/luci")
    print()
    print("✅ 有效凭证:")
    for user, pwd in VALID_CREDENTIALS.items():
        print(f"   - {user} / {pwd}")
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
