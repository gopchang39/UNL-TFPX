from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

# This ensures the CSV is created in the SAME folder as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'checklist_data.csv')

HEADERS = ["Task ID", "HDI check", "Sensor-ROC check", "Module gluing", "Spacer gluing", 
           "Wire bonding", "Pull test", "Carrier assembly", "Electrical test", "Shipped", "Row Notes"]

@app.route('/')
def index():
    # Ensure index.html is also found in the same directory
    index_path = os.path.join(BASE_DIR, 'index.html')
    return open(index_path).read()

@app.route('/save', methods=['POST'])
def save_data():
    try:
        data = request.json
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)
            for row in data:
                line = [row.get("id", "")]
                for col in HEADERS[1:-1]:
                    c = row.get(col, {})
                    # Formatting the cell data into a readable string for the CSV
                    line.append(f"Time:{c.get('t','')} | Name:{c.get('n','')} | Note:{c.get('m','')}")
                line.append(row.get("rowNotes", ""))
                writer.writerow(line)
        
        print(f"--- Data successfully saved to: {CSV_FILE} ---")
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"Error saving CSV: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Initializing the file so it exists immediately
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)
    
    app.run(port=5000, debug=True)