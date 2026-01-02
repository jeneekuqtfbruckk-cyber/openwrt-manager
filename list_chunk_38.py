
import json
import os

try:
    with open('payload_chunk_38.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Total files: {len(data)}")
    for i, item in enumerate(data):
        print(f"{i}: {item['path']} ({len(item['content'])} bytes)")
except Exception as e:
    print(f"Error: {e}")
