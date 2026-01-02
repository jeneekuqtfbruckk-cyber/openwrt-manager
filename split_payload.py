import json
import os

INPUT_FILE = "push_payload.json"
CHUNK_SIZE = 5 # items per chunk

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    files = json.load(f)

for i in range(0, len(files), CHUNK_SIZE):
    chunk = files[i:i + CHUNK_SIZE]
    output_name = f"payload_chunk_{i//CHUNK_SIZE}.json"
    with open(output_name, "w", encoding="utf-8") as f:
        json.dump(chunk, f, ensure_ascii=False)
    print(f"Created {output_name} with {len(chunk)} files")
