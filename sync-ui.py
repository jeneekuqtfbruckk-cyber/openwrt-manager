import os
import shutil
import sys

# 配置路径
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MASTER_DIR = os.path.join(ROOT_DIR, "open-wrt-manager-ui (2)")
REPLICA_DIR = os.path.join(ROOT_DIR, "browser-extension")

# 要同步的资产清单 (Source -> Destination Relative Paths)
SYNC_MAP = [
    # 1. 全局样式 (Tailwind v4 Theme)
    {
        "src": os.path.join("app", "globals.css"),
        "dest": os.path.join("entrypoints", "popup", "globals.css") # 假设 WXT 结构
    },
    # 2. 基础 UI 组件 (Radix + Tailwind)
    {
        "src": os.path.join("components", "ui"),
        "dest": os.path.join("components", "ui"),
        "is_dir": True
    },
    # 3. 工具类 (cn, tailwind-merge)
    {
        "src": os.path.join("lib", "utils.ts"),
        "dest": os.path.join("utils", "cn.ts") # 稍微改个名适配插件习惯
    }
]

def sync_assets():
    print(f"🚀 Starting UI Sync: Master -> Replica")
    print(f"   From: {MASTER_DIR}")
    print(f"   To:   {REPLICA_DIR}\n")

    if not os.path.exists(MASTER_DIR):
        print(f"❌ Error: Master directory not found: {MASTER_DIR}")
        return
    
    if not os.path.exists(REPLICA_DIR):
        print(f"⚠️  Replica directory not found: {REPLICA_DIR}")
        print("   (Have you initialized the WXT project yet?)")
        return

    success_count = 0

    for item in SYNC_MAP:
        src_full = os.path.join(MASTER_DIR, item["src"])
        # 如果目标路径在 map 里定义了具体的 dest (比如 globals.css 可能放在 assets 下)，需要灵活处理
        # 这里简化处理：如果是目录，dest 就是目录；如果是文件，dest 就是文件
        dest_full = os.path.join(REPLICA_DIR, item["dest"])

        # 检查源是否存在
        if not os.path.exists(src_full):
            print(f"⚠️  Skipping missing source: {item['src']}")
            continue

        try:
            # 目录同步
            if item.get("is_dir"):
                if os.path.exists(dest_full):
                    shutil.rmtree(dest_full)
                shutil.copytree(src_full, dest_full)
                print(f"✅ Synced Dir:  {item['dest']}")
            
            # 文件同步
            else:
                # 确保父目录存在
                os.makedirs(os.path.dirname(dest_full), exist_ok=True)
                shutil.copy2(src_full, dest_full)
                print(f"✅ Synced File: {item['dest']}")
            
            success_count += 1
        except Exception as e:
            print(f"❌ Failed to sync {item['dest']}: {str(e)}")

    print(f"\n✨ Sync Complete! ({success_count} items updated)")
    print("👉 Now the Extension AI has the latest UI assets.")

if __name__ == "__main__":
    sync_assets()
