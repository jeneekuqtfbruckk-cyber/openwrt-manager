#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenWrt 登录表单诊断工具
快速检测设备使用的登录字段名和路径
"""

import asyncio
import aiohttp
import re
from bs4 import BeautifulSoup


async def diagnose_login_form(target_url):
    """
    诊断单个 OpenWrt 设备的登录表单
    
    Args:
        target_url: 目标设备 URL，例如 http://192.168.1.1
    """
    # 规范化 URL
    if not target_url.startswith(("http://", "https://")):
        target_url = f"http://{target_url}"
    
    print(f"\n{'='*60}")
    print(f"🔍 正在诊断: {target_url}")
    print(f"{'='*60}\n")
    
    # 常见的登录路径
    login_paths = [
        "/cgi-bin/luci",
        "/cgi-bin/luci/admin",
        "/login",
        "/",
    ]
    
    timeout = aiohttp.ClientTimeout(total=10)
    
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            for path in login_paths:
                login_url = f"{target_url.rstrip('/')}{path}"
                
                try:
                    print(f"📡 尝试路径: {path}")
                    
                    async with session.get(
                        login_url,
                        ssl=False,
                        allow_redirects=True
                    ) as response:
                        if response.status != 200:
                            print(f"   ⚠️  HTTP {response.status}")
                            continue
                        
                        html = await response.text()
                        
                        # 方法1: 使用 BeautifulSoup 解析
                        try:
                            soup = BeautifulSoup(html, 'html.parser')
                            
                            # 查找表单
                            form = soup.find('form')
                            if form:
                                print(f"   ✅ 找到登录表单！")
                                print(f"   表单 action: {form.get('action', '未指定')}")
                                print(f"   表单 method: {form.get('method', 'GET').upper()}")
                                
                                # 查找用户名字段
                                username_fields = soup.find_all('input', attrs={'type': 'text'})
                                password_fields = soup.find_all('input', attrs={'type': 'password'})
                                
                                print(f"\n   📋 表单字段:")
                                
                                if username_fields:
                                    for field in username_fields:
                                        name = field.get('name', '无名称')
                                        placeholder = field.get('placeholder', '')
                                        print(f"      👤 用户名字段: name=\"{name}\"")
                                        if placeholder:
                                            print(f"         (提示: {placeholder})")
                                else:
                                    print(f"      ⚠️  未找到文本输入框")
                                
                                if password_fields:
                                    for field in password_fields:
                                        name = field.get('name', '无名称')
                                        placeholder = field.get('placeholder', '')
                                        print(f"      🔒 密码字段: name=\"{name}\"")
                                        if placeholder:
                                            print(f"         (提示: {placeholder})")
                                else:
                                    print(f"      ⚠️  未找到密码输入框")
                                
                                # 查找隐藏字段（可能包含 Token）
                                hidden_fields = soup.find_all('input', attrs={'type': 'hidden'})
                                if hidden_fields:
                                    print(f"\n   🔐 隐藏字段（Token）:")
                                    for field in hidden_fields:
                                        name = field.get('name', '无名称')
                                        value = field.get('value', '')[:20]
                                        print(f"      - {name} = {value}...")
                                
                                print(f"\n   ✅ 诊断成功！")
                                return True
                        
                        except Exception as e:
                            print(f"   ⚠️  BeautifulSoup 解析失败: {e}")
                        
                        # 方法2: 使用正则表达式提取
                        print(f"\n   🔍 使用正则表达式提取...")
                        
                        # 提取 input 字段
                        input_pattern = r'<input[^>]*name=["\']([^"\']+)["\'][^>]*type=["\'](\w+)["\']'
                        matches = re.findall(input_pattern, html, re.IGNORECASE)
                        
                        if matches:
                            print(f"   📋 找到的输入字段:")
                            for name, input_type in matches:
                                print(f"      - name=\"{name}\" type=\"{input_type}\"")
                        
                        # 反向匹配（type 在 name 前面）
                        input_pattern2 = r'<input[^>]*type=["\'](\w+)["\'][^>]*name=["\']([^"\']+)["\']'
                        matches2 = re.findall(input_pattern2, html, re.IGNORECASE)
                        
                        if matches2:
                            for input_type, name in matches2:
                                if (name, input_type) not in matches:
                                    print(f"      - name=\"{name}\" type=\"{input_type}\"")
                        
                        if matches or matches2:
                            print(f"\n   ✅ 找到表单字段！")
                            return True
                
                except asyncio.TimeoutError:
                    print(f"   ⏱️  超时")
                except Exception as e:
                    print(f"   ❌ 错误: {str(e)[:50]}")
            
            print(f"\n   ⚠️  未找到有效的登录表单")
            return False
                    
    except Exception as e:
        print(f"\n❌ 诊断失败: {e}")
        return False


async def main():
    """主函数"""
    print("=" * 60)
    print("🔧 OpenWrt 登录表单诊断工具")
    print("=" * 60)
    
    # 提示用户输入
    print("\n请输入要诊断的设备地址，例如:")
    print("  - http://192.168.1.1")
    print("  - 192.168.1.1:8080")
    print("  - http://42.227.147.231:2020")
    print()
    
    target = input("请输入地址: ").strip()
    
    if not target:
        print("❌ 未输入地址，退出。")
        return
    
    # 执行诊断
    await diagnose_login_form(target)
    
    print(f"\n{'='*60}")
    print("✅ 诊断完成！")
    print("=" * 60)
    print("\n💡 根据上面的结果，您可以确定:")
    print("   1. 登录路径是什么")
    print("   2. 用户名字段名称")
    print("   3. 密码字段名称")
    print("   4. 是否需要 Token")
    print()


if __name__ == "__main__":
    # 安装依赖提示
    print("📦 请确保已安装依赖: pip install aiohttp beautifulsoup4")
    print()
    
    asyncio.run(main())
