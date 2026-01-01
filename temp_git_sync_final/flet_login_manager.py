"""
Flet-compatible LoginManager
将 PyQt Signal 机制改为回调函数,以便在 Flet 中使用
"""
import asyncio
import aiohttp
from typing import List, Dict, Callable, Optional

# ============================================================================
# 配置常量 (从 openwrt_manager.py 复制)
# ============================================================================

CREDENTIALS_LIST = [
    {"username": "root", "password": "password"},  # 默认优先
    {"username": "root", "password": "admin"},
    {"username": "admin", "password": "admin"},
    {"username": "ubnt", "password": "ubnt"},
    {"username": "root", "password": "123456"},
]

LOGIN_PATHS = [
    "/cgi-bin/luci",           # 标准 LuCI (OpenWrt 官方)
    "/cgi-bin/luci/admin",     # 部分定制版本
    "/login",                  # 简化路径
]

FIELD_NAME_VARIANTS = [
    {"username": "luci_username", "password": "luci_password"},  # 标准 LuCI
    {"username": "username", "password": "password"},            # 简化版
    {"username": "auth_username", "password": "auth_password"},  # 认证版
]


class FletLoginManager:
    """Flet 兼容的登录管理器"""
    
    def __init__(self, max_concurrent: int = 50):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self._tasks = []
        self._is_running = False
        
        # 回调函数 (替代 PyQt Signal)
        self.on_row_update: Optional[Callable] = None  # (row, status, user, pwd, notes)
        self.on_task_finished: Optional[Callable] = None  # ()
    
    async def detect_login(self, row: int, target_url: str) -> Dict:
        """
        探测单个 OpenWrt 设备的登录
        
        Args:
            row: 表格行号
            target_url: 目标 URL
            
        Returns:
            检测结果字典
        """
        async with self.semaphore:
            # 如果停止,直接返回
            if not self._is_running:
                return {"status": "已停止", "user": "", "password": "", "notes": "用户中止"}
            
            # 规范化 URL
            if not target_url.startswith(("http://", "https://")):
                target_url = f"http://{target_url}"
            
            # 配置超时
            timeout = aiohttp.ClientTimeout(total=10)
            
            try:
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    # 遍历不同的登录路径
                    for login_path in LOGIN_PATHS:
                        if not self._is_running:
                            break
                        
                        login_url = f"{target_url.rstrip('/')}{login_path}"
                        
                        # 步骤1: 先访问登录页面
                        try:
                            async with session.get(
                                login_url,
                                ssl=False,
                                allow_redirects=True
                            ) as init_response:
                                if init_response.status not in [200, 401, 403]:
                                    continue
                                await init_response.read()
                        except Exception:
                            continue
                        
                        # 步骤2: 尝试不同的凭证组合
                        for cred in CREDENTIALS_LIST:
                            if not self._is_running:
                                break
                                
                            username = cred["username"]
                            password = cred["password"]
                            
                            # 步骤3: 尝试不同的字段名变体
                            for field_variant in FIELD_NAME_VARIANTS:
                                if not self._is_running:
                                    break
                                
                                # 更新状态 (通过回调)
                                if self.on_row_update:
                                    self.on_row_update(
                                        row,
                                        f"尝试 {username}/***",
                                        "",
                                        "",
                                        f"路径:{login_path}"
                                    )
                                
                                try:
                                    # 构建表单数据
                                    data = {
                                        field_variant["username"]: username,
                                        field_variant["password"]: password
                                    }
                                    
                                    # 发送 POST 登录请求
                                    async with session.post(
                                        login_url,
                                        data=data,
                                        ssl=False,
                                        allow_redirects=False
                                    ) as response:
                                        # 检查是否登录成功
                                        cookies = response.cookies
                                        has_sysauth = any('sysauth' in str(cookie.key) for cookie in cookies.values())
                                        is_redirect = response.status in [302, 303]
                                        
                                        if has_sysauth or is_redirect:
                                            # 登录成功!
                                            if self.on_row_update:
                                                self.on_row_update(
                                                    row,
                                                    "登录成功",
                                                    username,
                                                    password,
                                                    f"路径:{login_path}"
                                                )
                                            return {
                                                "status": "登录成功",
                                                "user": username,
                                                "password": password,
                                                "notes": f"路径:{login_path}"
                                            }
                                
                                except Exception as e:
                                    # 此组合失败,继续下一个
                                    continue
                    
                    # 所有尝试均失败
                    if self.on_row_update:
                        self.on_row_update(row, "登录失败", "", "", "所有凭证均失败")
                    return {"status": "登录失败", "user": "", "password": "", "notes": "所有凭证均失败"}
            
            except asyncio.TimeoutError:
                if self.on_row_update:
                    self.on_row_update(row, "连接超时", "", "", "无法连接到设备")
                return {"status": "连接超时", "user": "", "password": "", "notes": ""}
            except Exception as e:
                if self.on_row_update:
                    self.on_row_update(row, "连接失败", "", "", str(e)[:50])
                return {"status": "连接失败", "user": "", "password": "", "notes": str(e)[:50]}
    
    async def batch_detect(self, targets: List[str]):
        """批量探测"""
        self._is_running = True
        self._tasks = []
        
        # 创建所有任务
        for idx, target in enumerate(targets):
            task = asyncio.create_task(self.detect_login(idx, target))
            self._tasks.append(task)
        
        # 等待所有任务完成
        await asyncio.gather(*self._tasks, return_exceptions=True)
        
        # 发送完成信号 (通过回调)
        if self.on_task_finished:
            self.on_task_finished()
    
    def stop(self):
        """停止所有任务"""
        self._is_running = False
        for task in self._tasks:
            if not task.done():
                task.cancel()
