# EARLY DETECTION OF AT-RISK STUDENTS 

## Executive Summary
Schools wait until final exams are graded to see if a student is struggling, which is often too late to offer meaningful help and leads to dropouts. An early warning system was built to predict which students might need help based on their daily habits, background, and early grades. This includes a complete pipeline from initial data exploration to a fully functional web application. The system will be tested in real-world classrooms, updated to support students with special needs, and turned into a mobile app.

## Business Problem
Currently, educational institutions rely heavily on end-of-term exams to determine whether a student is failing. Because this information comes at the very end of the learning period, teachers miss the chance to step in early with tutoring or counselling. As a result, struggling students are left vulnerable to failing their classes, delaying their graduation, or dropping out of school entirely. Schools need a proactive tool that alerts teachers early in the semester when a student begins to fall behind.

## Methodology
* Data Collection and Preparation: Gathered historical records for 395 students, focusing on 13 key features like prior grades, absences, study time, and parental education. Cleaned and organized this information to remove errors and prepare it for analysis.
* Predictive Modelling: Trained a computer model to study this data and recognize the common warning signs of academic failure. The model was specifically tuned to prioritize catching the students who need help the most.
* Web Application: Built a simple, interactive web page where teachers can type in a single student's information or upload a spreadsheet of an entire class to instantly see who needs help and receive dynamic, actionable recommendations.

## Skills
* Data Analysis & Preparation: Python, Pandas, NumPy, Jupyter Notebook
* Predictive Modelling: Machine Learning, Scikit-Learn, Random Forest Classifier
* Web Application Development: Flask, HTML5, CSS3, Jinja2
* Model Deployment: Joblib (for saving and integrating the predictive model)

## Results and Business Recommendation
* Results: The predictive tool was highly successful, achieving an overall accuracy rate of 91.1%. It revealed that a student's most recent grades are the strongest predictors of their future performance, followed closely by a poor attendance record. The model was highly effective at ensuring struggling students do not slip through the cracks, successfully catching 88.5% of actual at-risk students.
* Business Recommendation: Educational institutions should adopt this early warning system to map out support plans. By grouping students into high, moderate, and low-risk categories, school administrators can step in early and provide targeted interventions—like  tutoring and peer mentoring—before a student officially fails.

## Next Steps
* Test the tool in two to three different schools to see how it performs across various real-world classrooms.
* Update the system to better evaluate and support students with special needs and physical impairments.
* Connect the tool directly to the school's existing student databases so teachers do not have to type in information manually.
* Develop a mobile app version for smartphones so educators can get instant alerts and check on their students from anywhere.
