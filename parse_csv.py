import sys
import csv
import os
import codecs

# ✅ Force UTF-8 encoding for Windows CMD
sys.stdout.reconfigure(encoding='utf-8')

if len(sys.argv) < 2:
    print("❌ ERROR: No CSV file provided!")
    sys.exit(1)

csv_file = sys.argv[1]

try:
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)

    if len(data) < 2:
        print("❌ ERROR: CSV file must have at least a header and one data row!")
        sys.exit(1)

    headers = data[0]
    rows = data[1:]

    print("\n🎯 Processed CSV Data:")
    print(headers)
    for row in rows:
        print(row)

except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)
