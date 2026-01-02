import os
import json

ROOT_DIR = r"e:\xcode\openwrt-manager"
FRONTEND_DIR_NAME = "open-wrt-manager-ui (2)"
OUTPUT_FILE = "push_payload.json"

EXCLUDE_DIRS = {
    "node_modules", ".next", "dist", "build", "__pycache__", ".git", ".vs", ".idea", "vscode", "locales"
}
EXCLUDE_EXTS = {
    ".exe", ".7z", ".zip", ".pyc", ".spec", ".log", ".pack", ".bin", ".dll", ".dat", ".pak", ".ico", ".png", ".jpg", ".svg" # Skip images/binaries for now
}

files_to_push = []

def is_text_file(filename):
    return not any(filename.lower().endswith(ext) for ext in EXCLUDE_EXTS)

for root, dirs, files in os.walk(ROOT_DIR):
    # Modify dirs in-place to skip ignored directories
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    
    for file in files:
        if not is_text_file(file):
            continue
            
        full_path = os.path.join(root, file)
        rel_path = os.path.relpath(full_path, ROOT_DIR)
        
        # Rename logic
        remote_path = rel_path
        if rel_path.startswith(FRONTEND_DIR_NAME):
            remote_path = rel_path.replace(FRONTEND_DIR_NAME, "frontend", 1)
        
        # Read content
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            files_to_push.append({
                "path": remote_path.replace("\\", "/"),
                "content": content
            })
        except Exception as e:
            print(f"Skipping {rel_path}: {e}")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(files_to_push, f, ensure_ascii=False)

print(f"Prepared {len(files_to_push)} files.")
