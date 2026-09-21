# Early Detection of At-Risk Students: Predictive Analytics Deployment

## Executive Summary
Educational institutions frequently rely on end-of-term examinations to assess academic performance, a lagging indicator that identifies failure only after it has occurred. This reactive approach contributes to higher dropout rates, delaying graduation and impacting institutional funding and reputation. To solve this, I engineered an end-to-end Machine Learning pipeline—deployed as an interactive web application—that predicts student failure using early-stage behavioral and academic metrics. The model acts as an early warning system, equipping educators with actionable insights to deploy targeted interventions before academic failure becomes irreversible.

## Business Problem
Schools currently lack proactive visibility into student performance, resulting in a misallocation of tutoring and counseling resources. Without a data-driven method to triage students by risk level early in the semester, administrators miss the critical window to intervene. The objective of this project is to shift the institutional strategy from reactive remediation to proactive risk mitigation.
## Methodology
* Data Engineering & Feature Selection: Processed a dataset of 395 historical student records. Conducted feature engineering on 13 variables—including attendance, study intervals, and prior academic performance—to isolate the highest-impact predictors of academic success.
* Predictive Analytics (Machine Learning): Trained and optimized a Random Forest Classifier to identify patterns of academic distress. The model was specifically tuned to maximize recall (sensitivity), prioritizing the identification of high-risk students to minimize false negatives (failing to catch a struggling student).
* Application Deployment & UI/UX: Developed an interactive web application using Flask, allowing educators to input individual student data or execute bulk batch predictions via CSV uploads, instantly generating risk assessments.

## Core Competencies Demonstrated
* Data Analysis: Python, Pandas, NumPy, Jupyter Notebook(Exploratory Data Analysis, Feature Engineering).
* Predictive Modelling: Scikit-Learn, Random Forest Classifier
* Web Application Development: Flask, HTML5, CSS3, JavaScript
* Model Integration: Joblib (Serialization and API Integration)

## Results & Business Intelligence Insights
* High-Fidelity Risk Detection: The predictive engine achieved an overall accuracy of 91.1%. More importantly for risk mitigation, it successfully identified 88.5% of actual at-risk students, ensuring highly vulnerable individuals do not slip through the cracks.
* Leading Indicators Identified: The algorithm revealed that early-term grades and attendance velocity are the strongest leading indicators of final academic outcomes, carrying significantly more weight than demographic background variables.
* Resource Allocation Triage: By stratifying students into high, moderate, and low-risk tiers, the application allows administrators to optimize their intervention budgets, directing intensive tutoring resources specifically to the highest-risk cohorts.

## Strategic Recommendations & Next Steps
* System Integration (ETL Pipeline): Connect the Flask application directly to the school's existing Student Information System (SIS) via API, eliminating the need for manual data entry and enabling real-time, automated risk dashboards for educators.
* Pilot Deployment & Validation: Execute a localized pilot program across three distinct academic departments to validate model performance across varied grading structures and behavioral norms.
* Feature Expansion for Accessibility: Update the predictive parameters to account for specialized learning accommodations, ensuring the model accurately evaluates students with physical impairments or special educational needs.
* Cross-Platform Accessibility: Develop a mobile-optimized interface, allowing counselors and educators to receive automated push-notification alerts regarding high-risk students in real time.
