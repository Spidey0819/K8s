from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Path to the persistent volume 
PV_DIR = "/dhruv_PV_dir"

def validate_csv_format(file_path):
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Check if required columns exist
        required_columns = ['product', 'amount']
        if not all(col in df.columns for col in required_columns):
            return False, None
            
        return True, df
    except Exception as e:
        return False, None

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        filename = data.get('file')
        product = data.get('product', '')
        
        file_path = os.path.join(PV_DIR, filename)
        
        # Validate CSV format
        is_valid, df = validate_csv_format(file_path)
        if not is_valid:
            return jsonify({
                "file": filename,
                "error": "Input file not in CSV format."
            }), 400
        
        # Calculate sum for the specified product
        try:
            product_sum = int(df[df['product'] == product]['amount'].sum())
            
            return jsonify({
                "file": filename,
                "sum": product_sum
            })
            
        except Exception as e:
            return jsonify({
                "file": filename,
                "error": "Error processing CSV data."
            }), 500
            
    except Exception as e:
        return jsonify({
            "file": filename if filename else None,
            "error": "Invalid JSON input."
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)