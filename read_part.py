
import sys
import os

file_path = r"e:\xcode\openwrt-manager\open-wrt-manager-ui (2)\package-lock.json"
start = int(sys.argv[1])
length = int(sys.argv[2])

try:
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        f.seek(start)
        data = f.read(length)
        print(data, end='')
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
