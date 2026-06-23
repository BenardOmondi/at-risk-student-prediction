from flask import Flask, render_template, request, send_file
import joblib
import secrets
import numpy as np
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# Load model
print("Loading model...")

try:
    model = joblib.load('model/at_risk_model.joblib')
    feature_names = [
        'age', 'Medu', 'Fedu', 'studytime', 'failures', 'absences', 'G1', 'G2',
        'sex_M', 'address_U', 'schoolsup_yes', 'famsup_yes', 'internet_yes'
    ]
    
    print("Model loaded successfully!")
    print(f"Expected features ({len(feature_names)}): {feature_names}")
    
except Exception as e:
    print(f"Error: {e}")
    model = None


# Prediction function for single student
def predict_student(student_data):
    if model is None:
        return {'error': 'Model not loaded'}
    
    try:
        # Create feature array in exact order from training
        features = [
            float(student_data['age']),
            float(student_data['Medu']),
            float(student_data['Fedu']),
            float(student_data['studytime']),
            float(student_data['failures']),
            float(student_data['absences']),
            float(student_data['G1']),
            float(student_data['G2']),
            # Categorical features (encoded as 0 or 1)
            1.0 if str(student_data['sex']).upper() == 'M' else 0.0,  # sex_M
            1.0 if str(student_data['address']).upper() == 'U' else 0.0,  # address_U
            1.0 if str(student_data['schoolsup']).lower() == 'yes' else 0.0,  # schoolsup_yes
            1.0 if str(student_data.get('famsup', 'no')).lower() == 'yes' else 0.0,  # famsup_yes
            1.0 if str(student_data['internet']).lower() == 'yes' else 0.0,  # internet_yes
        ]
        
        features_array = np.array(features).reshape(1, -1)
        
        # Predict
        prediction = model.predict(features_array)[0]
        probability = model.predict_proba(features_array)[0]
        
        result = {
            'prediction': 'At-Risk' if prediction == 1 else 'Safe',
            'risk_probability': float(probability[1] * 100),
            'safe_probability': float(probability[0] * 100)
        }
        
        return result
        
    except Exception as e:
        return {'error': f"Prediction error: {str(e)}"}

# Batch prediction function - vectorized for speed
def predict_batch(df):
    """Optimized batch prediction using vectorization"""
    if model is None:
        return []
    
    try:
        # Prepare feature matrix for all students at once
        features_list = []
        
        for idx, row in df.iterrows():
            features = [
                float(row['age']),
                float(row['Medu']),
                float(row['Fedu']),
                float(row['studytime']),
                float(row['failures']),
                float(row['absences']),
                float(row['G1']),
                float(row['G2']),
                1.0 if str(row['sex']).upper() == 'M' else 0.0,
                1.0 if str(row['address']).upper() == 'U' else 0.0,
                1.0 if str(row['schoolsup']).lower() == 'yes' else 0.0,
                1.0 if str(row.get('famsup', 'no')).lower() == 'yes' else 0.0,
                1.0 if str(row['internet']).lower() == 'yes' else 0.0,
            ]
            features_list.append(features)
        
        # Convert to numpy array (vectorized operations)
        features_array = np.array(features_list)
        
        # Make all predictions at once
        predictions = model.predict(features_array)
        probabilities = model.predict_proba(features_array)
        
        # Format results
        results = []
        for idx, (pred, prob) in enumerate(zip(predictions, probabilities)):
            results.append({
                'prediction': 'At-Risk' if pred == 1 else 'Safe',
                'risk_probability': float(prob[1] * 100),
                'safe_probability': float(prob[0] * 100)
            })
        
        return results
        
    except Exception as e:
        print(f"Batch prediction error: {e}")
        return []

# Routes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            student_data = {
                'age': int(request.form.get('age', 17)),
                'Medu': int(request.form.get('medu', 0)),
                'Fedu': int(request.form.get('fedu', 0)),
                'studytime': int(request.form.get('studytime', 1)),
                'failures': int(request.form.get('failures', 0)),
                'absences': int(request.form.get('absences', 0)),
                'G1': int(request.form.get('g1', 0)),
                'G2': int(request.form.get('g2', 0)),
                'sex': request.form.get('sex', 'M'),
                'address': request.form.get('address', 'U'),
                'schoolsup': request.form.get('schoolsup', 'no'),
                'famsup': request.form.get('famsup', 'no'),
                'internet': request.form.get('internet', 'yes')
            }
            
            # Predict
            result = predict_student(student_data)
            
            # Check for errors
            if 'error' in result:
                return render_template('predict.html', error=result['error'])
            
            # Get risk factors
            risk_factors = []
            if student_data['G1'] < 10:
                risk_factors.append(f"Low G1 ({student_data['G1']}/20)")
            if student_data['G2'] < 10:
                risk_factors.append(f"Low G2 ({student_data['G2']}/20)")
            if student_data['failures'] > 0:
                risk_factors.append(f"{student_data['failures']} past failures")
            if student_data['absences'] > 10:
                risk_factors.append(f"High absences ({student_data['absences']})")
            if student_data['studytime'] == 1:
                risk_factors.append("Very low study time")
            if student_data['internet'].lower() == 'no':
                risk_factors.append("No internet access")
            
            result['risk_factors'] = risk_factors
            
            return render_template('results.html', result=result, student=student_data)
            
        except Exception as e:
            return render_template('predict.html', error=f"Error: {str(e)}")
    
    return render_template('predict.html')

@app.route('/batch', methods=['GET', 'POST'])
def batch():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('batch.html', error="No file uploaded")
        
        file = request.files['file']
        
        if file.filename == '' or not file.filename.endswith('.csv'):
            return render_template('batch.html', error="Please upload a CSV file")
        
        try:
            df = pd.read_csv(file)
            
            # Check for required columns
            required = ['age', 'Medu', 'Fedu', 'studytime', 'failures', 'absences', 
                       'G1', 'G2', 'sex', 'address', 'schoolsup', 'famsup', 'internet']
            missing = [col for col in required if col not in df.columns]
            
            if missing:
                return render_template('batch.html', 
                    error=f"Missing columns: {', '.join(missing)}")
            
            # Use vectorized batch prediction for speed
            batch_results = predict_batch(df)
            
            # Build results with metadata
            results = []
            for idx, batch_result in enumerate(batch_results):
                if 'error' not in batch_result:
                    results.append({
                        'index': idx + 1,
                        'student_id': df.iloc[idx].get('student_id', f'STD{idx+1:03d}'),
                        'name': df.iloc[idx].get('name', f'Student {idx+1}'),
                        'prediction': batch_result['prediction'],
                        'risk': batch_result['risk_probability']
                    })
            
            at_risk = sum(1 for r in results if r['prediction'] == 'At-Risk')
            
            return render_template('batch_result.html',
                                 results=results,
                                 total=len(results),
                                 at_risk=at_risk,
                                 safe=len(results) - at_risk)
            
        except Exception as e:
            return render_template('batch.html', error=f"Error: {str(e)}")
    
    return render_template('batch.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/download/template')
def download_template():
    template_data = {
        'student_id': ['001', '002', '003'],
        'name': ['Student A', 'Student B', 'Student C'],
        'age': [17, 18, 16],
        'Medu': [3, 2, 4],
        'Fedu': [3, 1, 4],
        'studytime': [2, 1, 3],
        'failures': [0, 1, 0],
        'absences': [3, 15, 2],
        'G1': [12, 8, 15],
        'G2': [11, 7, 14],
        'sex': ['M', 'F', 'M'],
        'address': ['U', 'R', 'U'],
        'schoolsup': ['no', 'yes', 'no'],
        'famsup': ['no', 'yes', 'no'], 
        'internet': ['yes', 'no', 'yes']
    }
    
    df = pd.DataFrame(template_data)
    df.to_csv('template.csv', index=False)
    
    return send_file('template.csv',
                    as_attachment=True,
                    download_name='student_template.csv')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)