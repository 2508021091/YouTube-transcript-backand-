from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "TextFinder Backend is running!"

@app.route("/test")
def test():
    return jsonify({
        "success": True,
        "message": "Backend connection is working!"
    })

if __name__ == "__main__":
    app.run()
