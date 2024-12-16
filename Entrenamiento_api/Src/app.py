from flask import Flask, request, jsonify

app = Flask(__name__)

# Variable global para gestionar el valor
value = None

# GET /value
@app.route('/value', methods=['GET'])
def get_value():
    global value
    if value is None:
        return jsonify({"error": "Value not set"}), 404
    return jsonify({"value": value}), 200

# POST /value
@app.route('/value', methods=['POST'])
def create_value():
    global value
    if value is not None:
        return jsonify({"error": "Value already set"}), 400

    data = request.get_json()
    if not data or 'value' not in data or not isinstance(data['value'], str):
        return jsonify({"error": "Invalid input. 'value' must be a string"}), 400

    value = data['value']
    return jsonify({"message": "Value created successfully", "value": value}), 201

# PUT /value
@app.route('/value', methods=['PUT'])
def update_value():
    global value
    if value is None:
        return jsonify({"error": "No value to update"}), 404

    data = request.get_json()
    if not data or 'value' not in data or not isinstance(data['value'], str):
        return jsonify({"error": "Invalid input. 'value' must be a string"}), 400

    value = data['value']
    return jsonify({"message": "Value updated successfully", "value": value}), 200

# DELETE /value
@app.route('/value', methods=['DELETE'])
def delete_value():
    global value
    if value is None:
        return jsonify({"error": "No value to delete"}), 404

    value = None
    return jsonify({"message": "Value deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
