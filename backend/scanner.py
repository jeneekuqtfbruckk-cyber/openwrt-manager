import asyncio
import aiohttp
import urllib.parse
from typing import Dict, List

# ============================================================================
# Configuration from original openwrt_manager.py
# ============================================================================

CREDENTIALS_LIST = [
    {"username": "root", "password": "password"},
    {"username": "root", "password": "admin"},
    {"username": "admin", "password": "admin"},
    {"username": "ubnt", "password": "ubnt"},
    {"username": "root", "password": "123456"},
    {"username": "root", "password": "password123"}, # Added common variation
    {"username": "admin", "password": "password"},
]

LOGIN_PATHS = [
    "/cgi-bin/luci",
    "/cgi-bin/luci/admin",
    "/",  # Added root as fallback
]

FIELD_NAME_VARIANTS = [
    {"username": "luci_username", "password": "luci_password"},
    {"username": "username", "password": "password"},
    {"username": "auth_username", "password": "auth_password"},
]

# ============================================================================
# Core Logic
# ============================================================================

async def check_openwrt(target_url, timeout=10) -> Dict:
    """
    Robust OpenWrt detection ported from LoginManager.detect_login
    """
    # Normalize URL
    if not target_url.startswith(("http://", "https://")):
        target_url = f"http://{target_url}"
    
    # Common headers to mimic browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # Use a single session for all attempts on this target
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=timeout),
            headers=headers,
            connector=aiohttp.TCPConnector(ssl=False) # Important: Ignore SSL errors
        ) as session:
            
            # 1. Iterate through Login Paths
            for login_path in LOGIN_PATHS:
                full_login_url = f"{target_url.rstrip('/')}{login_path}"
                
                try:
                    # Initial GET to check availability & get cookies/tokens
                    async with session.get(full_login_url) as response:
                        if response.status not in [200, 401, 403]:
                            continue # Path not valid
                        
                        # Consume body
                        await response.read()

                    # 2. Iterate Credentials
                    for cred in CREDENTIALS_LIST:
                        username = cred["username"]
                        password = cred["password"]

                        # 3. Iterate Field Variants
                        for field_variant in FIELD_NAME_VARIANTS:
                            form_data = {
                                field_variant["username"]: username,
                                field_variant["password"]: password
                            }

                            try:
                                async with session.post(full_login_url, data=form_data, allow_redirects=False) as post_response:
                                    # Logic from original app: Check cookies and redirects for success
                                    cookies = post_response.cookies
                                    has_sysauth = any('sysauth' in str(cookie.key) for cookie in cookies.values())
                                    is_redirect = post_response.status in [302, 303]

                                    if has_sysauth or is_redirect:
                                        # SUCCESS!
                                        return {
                                            "address": target_url,
                                            "status": "success",
                                            "username": username,
                                            "password": password,
                                            "details": f"{login_path} | {username}"
                                        }
                                    
                                    # Fail fast for this credential if not 404/500
                                    if post_response.status not in [404, 500]:
                                        break # Password wrong, try next credential (skip other field variants)

                            except Exception:
                                continue # Try next VARIANT

                except Exception:
                   continue # Try next PATH

            # If loop finishes without success
            return {
                "address": target_url,
                "status": "failed",
                "details": "Login Failed"
            }

    except asyncio.TimeoutError:
         return {"address": target_url, "status": "failed", "details": "Timeout"}
    except aiohttp.ClientConnectorError:
         return {"address": target_url, "status": "failed", "details": "Connection Refused"}
    except Exception as e:
         return {"address": target_url, "status": "failed", "details": str(e)[:50]}


# Scanner Manager to handle concurrency
class ScannerManager:
    def __init__(self):
        self.is_running = False
        self.results = []
    
    async def run_scan(self, targets: list, concurrency: int = 50, callback=None):
        self.is_running = True
        self.results = []
        
        sem = asyncio.Semaphore(concurrency)
        
        async def worker(ip):
            async with sem:
                if not self.is_running: return
                result = await check_openwrt(ip)
                # Parse result and enrich
                result['id'] = len(self.results) + 1
                self.results.append(result)
                if callback:
                    await callback(result)
                    
        tasks = [worker(ip) for ip in targets]
        # Allow cancellation
        try:
            await asyncio.gather(*tasks)
        except Exception:
            pass
        finally:
            self.is_running = False
