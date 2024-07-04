from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load model and encoded values
model = joblib.load("model_small.pkl")
label_encoder = joblib.load('label_encoder.pkl')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/predict')
def predict():
    return render_template("predict.html")

@app.route('/output', methods=["POST"])
def output():
    if request.method == 'POST':
        city = request.form["city"].strip()
        pm25 = float(request.form["pm25"])
        pm10 = float(request.form["pm10"])
        no2 = float(request.form["no2"])
        co = float(request.form["co"])
        so2 = float(request.form["so2"])
        o3 = float(request.form["o3"])
        date = request.form["date"]

        # Ensure the city name is valid
        if city not in label_encoder.classes_:
            return render_template("output.html", y="Invalid City", z="Please enter a valid city name.")

        # Transform city and date fields
        city_encoded = label_encoder.transform([city])[0]
        year = int(date.split('-')[0])
        month = int(date.split('-')[1])

        # Create a DataFrame for the input features
        feature_cols = ['City', 'PM2.5', 'PM10', 'NO2', 'CO', 'SO2', 'O3', 'Year', 'Month']
        data = pd.DataFrame([[city_encoded, pm25, pm10, no2, co, so2, o3, year, month]], columns=feature_cols)

        # Make prediction
        pred = model.predict(data)
        pred = pred[0]

        # Determine AQI category
        if pred >= 0 and pred < 50:
            res = 'GOOD'
        elif pred >= 50 and pred < 100:
            res = 'SATISFACTORY'
        elif pred >= 100 and pred < 200:
            res = 'MODERATELY POLLUTED'
        elif pred >= 200 and pred < 300:
            res = 'POOR'
        elif pred >= 300 and pred < 400:
            res = 'VERY POOR'
        else:
            res = 'SEVERE'

        return render_template("output.html", y=f"AQI: {str(pred)}", z=res)

if __name__ == "__main__":
    app.run(debug=True)
