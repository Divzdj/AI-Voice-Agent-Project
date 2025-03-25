from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/api/logs', methods=['GET'])
def get_logs():
    try:
        with open('conversation_log.json', 'r') as f:
            logs = json.load(f)
        return jsonify(logs)
    except FileNotFoundError:
        return jsonify([])

if __name__ == '__main__':
    app.run(port=5001, debug=True) # Run on a different port than your main app