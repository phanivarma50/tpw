
from flask import Flask, request, render_template, jsonify
import joblib

app = Flask(__name__)

# Load the trained model and vectorizer
model = joblib.load("phishing_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    url = request.form.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    # Transform input URL
    url_transformed = vectorizer.transform([url])

    # Predict phishing or not (0 = Safe, 1 = Phishing)
    prediction = model.predict(url_transformed)
    
    result = "Phishing" if prediction == 0 else "Safe"
    
    return render_template("index.html", url=url, prediction=result)

if __name__ == "__main__":
    app.run(debug=True)
