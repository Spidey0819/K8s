from flask import Flask, request, jsonify
import requests
import os
import json

app = Flask(__name__)

# Container 2's URL (using Kubernetes service name)
CONTAINER2_URL = "http://container2-service:5000/process"

# Path to the persistent volume (replace 'yourname' with your first name)
PV_DIR = "/yourname_PV_dir"

@app.route('/store-file', methods=['POST'])
def store_file():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Check if file parameter exists and is not null
        if not data or 'file' not in data or data['file'] is None:
            return jsonify({
                "file": None,
                "error": "Invalid JSON input."
            }), 400
        
        filename = data['file']
        file_data = data.get('data', '')
        
        # Ensure directory exists
        os.makedirs(PV_DIR, exist_ok=True)
        
        # Write to file in persistent volume
        try:
            filepath = os.path.join(PV_DIR, filename)
            with open(filepath, 'w') as f:
                f.write(file_data)
            
            return jsonify({
                "file": filename,
                "message": "Success."
            }), 200
        except Exception as e:
            return jsonify({
                "file": filename,
                "error": "Error while storing the file to the storage."
            }), 500
            
    except Exception as e:
        return jsonify({
            "file": None,
            "error": "Invalid JSON input."
        }), 400

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Check if file parameter exists and is not null
        if not data or 'file' not in data or data['file'] is None:
            return jsonify({
                "file": None,
                "error": "Invalid JSON input."
            }), 400
        
        # Get filename and check if file exists in persistent volume
        filename = data['file']
        filepath = os.path.join(PV_DIR, filename)
        if not os.path.exists(filepath):
            return jsonify({
                "file": filename,
                "error": "File not found."
            }), 404

        # Forward request to container2
        try:
            response = requests.post(
                CONTAINER2_URL,
                json={
                    "file": filename,
                    "product": data.get("product", "")
                }
            )
            return response.json(), response.status_code
            
        except requests.exceptions.RequestException as e:
            return jsonify({
                "file": filename,
                "error": "Error communicating with processing service."
            }), 500

    except Exception as e:
        return jsonify({
            "file": None,
            "error": "Invalid JSON input."
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)