from flask import Flask,request,render_template, jsonify,Response,make_response
from flask_cors import CORS

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Allow requests from React frontend
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})




# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})

# CORS(app)
@app.route('/api_test', methods=['POST','OPTIONS'])
def api_test():
    try:
        return {"status":"success"}
    except Exception as e:
        print(e)
        return Response(status=500)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run()
