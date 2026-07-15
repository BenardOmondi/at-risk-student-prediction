# EARLY DETECTION OF AT-RISK STUDENTS USING RANDOM FOREST MODEL

## Overview
This project is an end-to-end predictive analytics system designed to identify students at risk of academic underperformance. By 
leveraging historical student performance and demographic data, the system provides early warning indicators to educators, allowing for 
timely and targeted interventions. 

The project encompasses a complete machine learning pipeline—from exploratory data analysis and feature engineering in Jupyter Notebook to
a fully functional, container-ready web application built with Flask.

## Key Features
* Individual Risk Assessment: A user-friendly web interface allowing educators to input student metrics and receive real-time risk
probabilities.
* Batch Processing: Bulk upload capabilities via CSV for processing entire classrooms or schools simultaneously.
* Feature Importance Analysis: Transparent identification of key risk factors (e.g., prior grades, absences, study time, and parental 
education).
* Actionable Insights: Dynamic generation of recommended interventions based on specific risk triggers.

## Technology Stack
* Data Science & Modelling: Python, Pandas, Scikit-Learn, NumPy, Jupyter Notebook
* Machine Learning: Random Forest Classifier (Optimized via Hyperparameter Tuning).
* Web Framework: Flask, Jinja2, HTML5/CSS3
* Model Serialization: Joblib.

## Model Performance
The core of the system is a Random Forest model trained on 395 student records with 13 key features. The model prioritizes identifying
at-risk students, achieving strong cross-validated results:
* Accuracy: 91.1%.
* Recall (Sensitivity): 88.5% (Successfully identifying actual at-risk students).
* Precision: 85.2%.
* F1-Score: 86.8%.
