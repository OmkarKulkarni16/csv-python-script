import sys
import csv

# ✅ Force UTF-8 encoding for Windows CMD
sys.stdout.reconfigure(encoding='utf-8')

# Define the required fields to extract
REQUIRED_FIELDS = {
    "API Name",
    "Service Endpoint/URI in Policy Manager",
    "API Category (HIGH/MEDIUM/LOW)",
    "Backend Service URL for Routing",
    "Fields Captured from Request for logging (Variable_Name = JSONPath)",
    "Fields Captured from Response for logging",
    "API Gateway Error Structure",
    "Response Field for success validation",
    "Success response",
    "Target Server name"
}

def clean_value(value):
    """Removes non-ASCII and special characters from extracted values."""
    return value.replace('\n', ' ').encode("ascii", "ignore").decode()

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

    # Create a dictionary filtering only required fields and cleaning values
    filtered_data = {
        header: clean_value(row[i])  # ✅ Ensure ASCII-compatible output
        for i, header in enumerate(headers) if header in REQUIRED_FIELDS
    }

    print("\n🎯 Processed CSV Data (Filtered Fields):\n")
    for key, value in filtered_data.items():
        print(f"{key}: {value}")

except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)
