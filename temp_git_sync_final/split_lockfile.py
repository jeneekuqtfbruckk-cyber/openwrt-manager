
import os

source_file = r"e:\xcode\openwrt-manager\open-wrt-manager-ui (2)\package-lock.json"
output_dir = r"e:\xcode\openwrt-manager\temp_chunks"
lines_per_file = 800

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(source_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(0, len(lines), lines_per_file):
    chunk = lines[i:i + lines_per_file]
    output_filename = os.path.join(output_dir, f"lock_part_{i // lines_per_file:02d}.txt")
    with open(output_filename, 'w', encoding='utf-8') as out:
        out.writelines(chunk)
    print(f"Created {output_filename}")
