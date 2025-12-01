import json
import sys

fname = 'edudata.json'
out = 'edudata.utf8.json'
encodings = ['utf-8', 'utf-8-sig', 'utf-16', 'latin-1', 'cp1252']

for e in encodings:
    try:
        with open(fname, 'r', encoding=e) as f:
            data = f.read()
        # validate JSON
        json.loads(data)
        with open(out, 'w', encoding='utf-8') as f:
            f.write(data)
        print(f"Successfully read '{fname}' with encoding {e}, wrote '{out}' (utf-8).")
        sys.exit(0)
    except Exception as exc:
        print(f"Failed to read with {e}: {exc}")

print(f"All encodings failed for '{fname}'")
sys.exit(2)
