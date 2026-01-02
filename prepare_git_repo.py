import os
import shutil

ROOT_DIR = r"e:\xcode\openwrt-manager"
DEST_DIR = r"e:\xcode\openwrt-manager\temp_git_sync_final"
FRONTEND_DIR_NAME = "open-wrt-manager-ui (2)"

EXCLUDE_DIRS = {
    "node_modules", ".next", "dist", "build", "__pycache__", ".git", ".vs", ".idea", "vscode",
    "temp_git_sync", "temp_chunks", "_backup_v2_pyqt", "AI回复"
}

EXCLUDE_FILES = {
    "push_payload.json", "prepare_push.py", "split_payload.py", "read_part.py", "get_chunk_file.py",
    "list_chunk_38.py", "prepare_git_repo.py", "open-wrt-manager-ui.zip", "run_server.bat",
    "test_server.py"
}

def should_exclude_file(filename):
    if filename.startswith("payload_chunk_") and filename.endswith(".json"):
        return True
    if filename.startswith("temp_file_"):
        return True
    if filename in EXCLUDE_FILES:
        return True
    if filename.endswith(".pyc"):
        return True
    return False

def main():
    if os.path.exists(DEST_DIR):
        print(f"Cleaning {DEST_DIR}...")
        shutil.rmtree(DEST_DIR)
    os.makedirs(DEST_DIR)

    print(f"Copying files from {ROOT_DIR} to {DEST_DIR}...")
    
    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        # Determine relative path from root
        rel_root = os.path.relpath(root, ROOT_DIR)
        
        # Determine target directory structure
        target_rel_root = rel_root
        if rel_root == ".":
            target_rel_root = ""
        elif rel_root.startswith(FRONTEND_DIR_NAME):
            target_rel_root = rel_root.replace(FRONTEND_DIR_NAME, "frontend", 1)
        
        target_dir = os.path.join(DEST_DIR, target_rel_root)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
            
        for file in files:
            if should_exclude_file(file):
                continue
                
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_dir, file)
            
            try:
                shutil.copy2(src_file, dst_file)
                count += 1
            except Exception as e:
                print(f"Error copying {src_file}: {e}")

    print(f"Copied {count} files to {DEST_DIR}.")

if __name__ == "__main__":
    main()
