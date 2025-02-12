import sys
import csv
import re
from urllib.parse import urlparse

sys.stdout.reconfigure(encoding='utf-8')

REQUIRED_FIELDS = {
    "API Name",
    "Service Endpoint/URI in Policy Manager",
    "API Category (HIGH/MEDIUM/LOW)",
    "Backend Service URL for Routing",
    "Fields Captured from Request for logging",  # ✅ Ensure this field is extracted
    "Fields Captured from Response for logging",
    "API Gateway Error Structure",
    "Response Field for success validation",
    "Success response",
    "Target Server name"
}

def clean_value(value):
    """Removes non-ASCII and special characters from extracted values."""
    return value.replace('\n', ' ').strip().encode("ascii", "ignore").decode()

def extract_url_parts(url):
    """Extracts hostname, port, and backend path from a given URL."""
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        port = parsed_url.port if parsed_url.port else ("443" if parsed_url.scheme == "https" else "80")
        backend_path = parsed_url.path
        return hostname, str(port), backend_path
    except Exception:
        return None, None, None

if len(sys.argv) < 2:
    print("ERROR: No CSV file provided!")
    sys.exit(1)

csv_file = sys.argv[1]

try:
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)

    if len(data) < 2:
        print("ERROR: CSV file must have at least a header and one data row!")
        sys.exit(1)

    headers = data[0]
    row = data[1]  # Since there's only one row

    # Extract required fields
    filtered_data = {
        header: clean_value(row[i]) if i < len(row) else "N/A"
        for i, header in enumerate(headers) if header in REQUIRED_FIELDS
    }

    # ✅ Explicitly check if "Fields Captured from Request for logging" exists
    request_logging_fields = filtered_data.get("Fields Captured from Request for logging", "N/A")
    if request_logging_fields.strip() == "":
        request_logging_fields = "N/A"  # Prevent blank values

    # ✅ Print to Jenkins logs
    print("📝 Fields Captured from Request for Logging:")
    print(f"🔹 {request_logging_fields}")

    # ✅ Extract and Print Response Logging Fields Separately
    response_logging_fields = filtered_data.get("Fields Captured from Response for logging", "N/A")
    print("📄 Fields Captured from Response for Logging:")
    print(f"🔹 {response_logging_fields}")

    # Extract Hostname, Port, and Backend Path
    backend_url = filtered_data.get("Backend Service URL for Routing", "")
    hostname, port, backend_path = extract_url_parts(backend_url)

    print("📄 Processed CSV Data (Filtered Fields):")
    for key, value in filtered_data.items():
        print(f"🔹 {key}: {value}")

    if hostname and backend_path:
        print("🌍 Extracted URL Components:")
        print(f"🔹 Hostname: {hostname}")
        print(f"🔹 Port: {port}")
        print(f"🔹 Backend Path: {backend_path}")
    else:
        print("⚠️ Warning: Unable to extract hostname, port, or backend path from the URL.")

    # ✅ Save extracted values to a file for Jenkins
    with open("extracted_values.txt", "w") as f:
        for key, value in filtered_data.items():
            f.write(f"{key.upper().replace(' ', '_')}={value}\n")
        f.write(f"FIELDS_CAPTURED_FROM_REQUEST_FOR_LOGGING={request_logging_fields}\n")  # ✅ Ensure it's saved
        f.write(f"FIELDS_CAPTURED_FROM_RESPONSE_FOR_LOGGING={response_logging_fields}\n")
        f.write(f"HOSTNAME={hostname}\n")
        f.write(f"PORT={port}\n")
        f.write(f"BACKEND_PATH={backend_path}\n")

    print("✅ Extracted values saved to 'extracted_values.txt' for Jenkins.")

except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)
