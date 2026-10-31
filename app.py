from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load trained ML model
model = joblib.load("student_performance_model.pkl")

# Load feature columns used during training
feature_columns = joblib.load("feature_columns.pkl")


# -------------------------------
# Performance Level
# -------------------------------
def get_performance(grade):
    if grade >= 16:
        return "Excellent"
    elif grade >= 12:
        return "Good"
    elif grade >= 10:
        return "Average"
    else:
        return "Poor"


# -------------------------------
# Risk Level
# -------------------------------
def get_risk(grade):
    if grade < 10:
        return "High Risk"
    elif grade < 12:
        return "Medium Risk"
    else:
        return "Low Risk"


# -------------------------------
# Home Page
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------
# Prediction
# -------------------------------
@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        # Create input dataframe
        input_data = pd.DataFrame([{
            "age": int(data["age"]),
            "sex": data["sex"],
            "studytime": int(data["studytime"]),
            "failures": int(data["failures"]),
            "absences": int(data["absences"]),
            "Medu": int(data["Medu"]),
            "Fedu": int(data["Fedu"]),
            "goout": int(data["goout"]),
            "health": int(data["health"]),
            "internet": data["internet"],
            "G1": int(data["G1"]),
            "G2": int(data["G2"])
        }])

        # Convert categorical values into numerical columns
        input_data = pd.get_dummies(input_data)

        # Make columns exactly match training data
        input_data = input_data.reindex(
            columns=feature_columns,
            fill_value=0
        )

        # Predict final grade
        prediction = model.predict(input_data)[0]

        # Keep grade between 0 and 20
        prediction = max(0, min(20, prediction))

        performance = get_performance(prediction)
        risk = get_risk(prediction)

        return jsonify({
            "success": True,
            "predicted_grade": round(float(prediction), 2),
            "performance": performance,
            "risk": risk
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })


# -------------------------------
# Run Application
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)