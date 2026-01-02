

import json
import sys
import os

try:
    index = int(sys.argv[1])
    output_file = sys.argv[2]
    
    with open('payload_chunk_38.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 0 <= index < len(data):
        with open(output_file, 'w', encoding='utf-8') as out:
            out.write(data[index]['content'])
        print(f"Written to {output_file}")
    else:
        print("Index out of range", file=sys.stderr)
        sys.exit(1)
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)

