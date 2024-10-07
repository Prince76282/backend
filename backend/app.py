from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


client = MongoClient('mongodb+srv://new:new12345@cluster0.kh70f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['livestream_db']
overlays_collection = db['overlays']

@app.route('/api/overlays', methods=['GET'])
def get_overlays():
    overlays = list(overlays_collection.find({}))
    for overlay in overlays:
        overlay['_id'] = str(overlay['_id'])  # Convert ObjectId to string
    return jsonify(overlays), 200

@app.route('/api/overlays', methods=['POST'])
def create_overlay():
    data = request.json
    overlay = {
        'content': data['content'],
        'position': data['position'],
        'size': data['size']
    }
    overlays_collection.insert_one(overlay)
    return jsonify({"message": "Overlay created successfully!"}), 201

@app.route('/api/overlays/<overlay_id>', methods=['PUT'])
def update_overlay(overlay_id):
    data = request.json
    overlays_collection.update_one({'_id': overlay_id}, {"$set": {
        'content': data['content'],
        'position': data['position'],
        'size': data['size']
    }})
    return jsonify({"message": "Overlay updated successfully!"}), 200

@app.route('/api/overlays/<overlay_id>', methods=['DELETE'])
def delete_overlay(overlay_id):
    overlays_collection.delete_one({'_id': overlay_id})
    return jsonify({"message": "Overlay deleted successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True , port=5000)
