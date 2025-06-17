from flask import Flask, request, jsonify
from recommender import recommend_from_model

print("📦 Flask app is starting...")

app = Flask(__name__)

@app.route("/recommend", methods=["GET"])
def get_recommendations():
    user_id = request.args.get("user_id", type=int)
    if user_id is None:
        return jsonify({"error": "user_id parameter is required"}), 400

    results = recommend_from_model(user_id)
    return jsonify({
        "user_id": user_id,
        "recommendations": results
    })

if __name__ == "__main__":
    print("🚀 Flask app running on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
