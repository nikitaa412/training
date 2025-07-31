from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load model
model = pickle.load(open('model/house_model.pkl', 'rb'))
# Load feature names
feature_names = pickle.load(open('model/feature_names.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        location = request.form['location']
        sqft = float(request.form['sqft'])
        beds = int(request.form['beds'])
        baths = int(request.form['baths'])
        year_built = int(request.form['year_built'])

        # Build feature dictionary
        features = {
            'sqft': sqft,
            'beds': beds,
            'baths': baths,
            'year_built': year_built,
            'location_Chicago': 0,
            'location_Los Angeles': 0,
            'location_New York': 0,
            'location_Phoenix': 0,
            'location_Houston': 0
        }

        location_key = f'location_{location}'
        if location_key in features:
            features[location_key] = 1

        # Ensure correct feature order
        input_df = pd.DataFrame([features])[feature_names]

        prediction = model.predict(input_df)[0]
        return render_template('predict.html', prediction=round(prediction, 2))

    return render_template('predict.html', prediction=None)

if __name__ == '__main__':
    app.run(debug=True)
