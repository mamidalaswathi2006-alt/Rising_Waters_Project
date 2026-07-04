from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load trained model
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = pickle.load(
    open(os.path.join(BASE_DIR, "models", "flood_model.pkl"), "rb")
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/predict", methods=["POST"])
def predict():

    Temp = float(request.form["Temp"])
    Humidity = float(request.form["Humidity"])
    Cloud_Cover = float(request.form["Cloud Cover"])
    ANNUAL = float(request.form["ANNUAL"])
    Jan_Feb = float(request.form["Jan-Feb"])
    Mar_May = float(request.form["Mar-May"])
    Jun_Sep = float(request.form["Jun-Sep"])
    Oct_Dec = float(request.form["Oct-Dec"])
    avgjune = float(request.form["avgjune"])
    sub = float(request.form["sub"])


    data = np.array([[
        Temp,
        Humidity,
        Cloud_Cover,
        ANNUAL,
        Jan_Feb,
        Mar_May,
        Jun_Sep,
        Oct_Dec,
        avgjune,
        sub
    ]])


    prediction = model.predict(data)


    if prediction[0] == 1:
        result = "🌊 Flood Risk Detected"
    else:
        result = "✅ No Flood Risk"


    return render_template(
        "index.html",
        prediction=result
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)