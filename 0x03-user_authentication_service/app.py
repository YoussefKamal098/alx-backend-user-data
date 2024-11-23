from flask import Flask, jsonify

# Initialize Flask app
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    # Return a JSON response with a message
    return jsonify({"message": "Bienvenue"})

# Run the app on host 0.0.0.0 and port 5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)