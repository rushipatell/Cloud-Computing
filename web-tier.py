from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)
lookupPath = 'Classification Results on Face Dataset (1000 images).csv'
lookup = {}

def read_csv():
    global lookup
    with open(lookupPath, 'r') as csvFile:
        lookupCsv = csv.reader(csvFile)
        lookup = {row[0]: row[1] for row in lookupCsv}

read_csv()

@app.route('/', methods=['POST'])
def classify_image():
    try:
        inputFile = request.files['inputFile']
        filename = inputFile.filename
        baseFilename = os.path.splitext(filename)[0]
        label = lookup.get(baseFilename)
        if label is not None:
            data = baseFilename+':'+label
            return data, 200
        else:
            return jsonify({'error': f"Filename {baseFilename} not found in lookup"}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
