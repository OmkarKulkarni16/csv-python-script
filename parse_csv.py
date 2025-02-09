import sys
import csv

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
    row = data[1]  # Since there's only one row

    print("\n🎯 Processed CSV Data:\n")
    
    for header, value in zip(headers, row):
        clean_value = value.replace('\n', ' ')  # Remove newlines
        print(f"{header}: {clean_value}")

except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)
