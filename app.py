from flask import Flask, request, jsonify, render_template_string
import csv
import os

app = Flask(__name__)
CSV_FILE = 'checklist.csv'

# Initialize CSV with headers if it doesn't exist
COLUMNS = ["Task ID", "HDI check", "Sensor-ROC check", "Module gluing", "Spacer gluing", "Wire bonding", "Pull test", "Carrier assembly", "Electrical test", "Shipped"]

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/save', methods=['POST'])
def save_data():
    data = request.json
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS + ["Notes"]) # Header
        for row in data:
            writer.writerow(row)
    return jsonify({"status": "success"})

@app.route('/load', methods=['GET'])
def load_data():
    if not os.path.exists(CSV_FILE):
        return jsonify([])
    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        return jsonify(list(reader))

if __name__ == '__main__':
    app.run(port=5000, debug=True)