from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle

app = Flask(__name__)

# Load your trained model (update the path if needed)
model = pickle.load(open('model.pkl', 'rb'))

# Map user-friendly input to model input for categorical fields
def preprocess_input(data):
    # Example: data['thal'] is a string from the UI
    thal_map = {
        'Normal': 1,
        'Fixed Defect': 2,
        'Reversible Defect': 3
    }
    sex_map = {'Male': 1, 'Female': 0}
    cp_map = {
        'Typical Angina': 0,
        'Atypical Angina': 1,
        'Non-anginal Pain': 2,
        'Asymptomatic': 3
    }
    fbs_map = {'True': 1, 'False': 0}
    exang_map = {'Yes': 1, 'No': 0}
    restecg_map = {
        'Normal': 0,
        'ST-T Abnormality': 1,
        'Left Ventricular Hypertrophy': 2
    }
    slope_map = {
        'Upsloping': 0,
        'Flat': 1,
        'Downsloping': 2
    }
    # Convert all fields
    processed = [
        int(data['age']),
        sex_map[data['sex']],
        cp_map[data['cp']],
        int(data['trestbps']),
        int(data['chol']),
        fbs_map[data['fbs']],
        restecg_map[data['restecg']],
        int(data['thalach']),
        exang_map[data['exang']],
        float(data['oldpeak']),
        slope_map[data['slope']],
        int(data['ca']),
        thal_map[data['thal']]
    ]
    return np.array([processed])

@app.route('/')
def home():
    return render_template('index.html')

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    input_data = preprocess_input(data)
    prediction = model.predict(input_data)[0]
    result = 'Heart Disease Detected' if prediction == 1 else 'No Heart Disease'
    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)
