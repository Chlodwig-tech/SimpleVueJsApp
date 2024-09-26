from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/clicktransform/', methods=['GET', 'POST'])
def clicktransform():
    response_data = {
        "content": "Success!"
    }
    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
