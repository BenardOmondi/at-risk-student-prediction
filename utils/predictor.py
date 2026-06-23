import numpy as np
import pandas as pd
from typing import Dict, List, Union, Optional

class StudentPredictor:
    """
    Handles all prediction logic for student risk assessment
    """
    
    def __init__(self, model, feature_names: List[str]):
        """
        Initialize predictor with trained model
        
        Args:
            model: Trained scikit-learn model
            feature_names: List of feature names in correct order
        """
        self.model = model
        self.feature_names = feature_names
    
    def encode_features(self, data: Dict) -> Dict:
        """
        Encode categorical features to numeric values
        
        Args:
            data: Dictionary with student features
            
        Returns:
            Dictionary with encoded features
        """
        encoded = data.copy()
        
        # Binary encoding for yes/no fields
        encoded['schoolsup'] = int(str(data.get('schoolsup', '')).lower() in ['yes', 'y', '1', 'true'])
        encoded['famsup'] = int(str(data.get('famsup', '')).lower() in ['yes', 'y', '1', 'true'])
        encoded['internet'] = int(str(data.get('internet', '')).lower() in ['yes', 'y', '1', 'true'])
        
        # Binary encoding for gender
        encoded['sex'] = int(str(data.get('sex', '')).upper() in ['M', 'MALE', '1'])
        
        # Binary encoding for address
        encoded['address'] = int(str(data.get('address', '')).upper() in ['U', 'URBAN', '1'])
        
        return encoded
    
    def validate_input(self, data: Dict) -> tuple[bool, Optional[str]]:
        """
        Validate input data before prediction
        
        Args:
            data: Dictionary with student features
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check all required features present
        for feature in self.feature_names:
            if feature not in data:
                return False, f"Missing required feature: {feature}"
        
        # Validate ranges
        validations = {
            'G1': (0, 20, 'First period grade'),
            'G2': (0, 20, 'Second period grade'),
            'failures': (0, 4, 'Number of failures'),
            'absences': (0, 100, 'Number of absences'),
            'studytime': (1, 4, 'Study time'),
            'age': (15, 25, 'Age'),
            'Medu': (0, 4, "Mother's education"),
            'Fedu': (0, 4, "Father's education"),
        }
        
        for feature, (min_val, max_val, name) in validations.items():
            try:
                value = float(data[feature])
                if value < min_val or value > max_val:
                    return False, f"{name} must be between {min_val} and {max_val}"
            except (ValueError, TypeError):
                return False, f"{name} must be a valid number"
        
        return True, None
    
    def predict_single(self, student_data: Dict) -> Dict:
        """
        Make prediction for a single student
        
        Args:
            student_data: Dictionary with student features
            
        Returns:
            Dictionary with prediction results
        """
        try:
            # Validate input
            is_valid, error_msg = self.validate_input(student_data)
            if not is_valid:
                return {'error': error_msg}
            
            # Encode features
            encoded_data = self.encode_features(student_data)
            
            # Create feature array in correct order
            features = np.array([
                float(encoded_data[feat]) for feat in self.feature_names
            ]).reshape(1, -1)
            
            # Make prediction
            prediction = self.model.predict(features)[0]
            probabilities = self.model.predict_proba(features)[0]
            
            return {
                'prediction': 'At-Risk' if prediction == 1 else 'Safe',
                'prediction_code': int(prediction),
                'risk_probability': float(probabilities[1] * 100),
                'safe_probability': float(probabilities[0] * 100),
                'confidence': float(max(probabilities) * 100)
            }
            
        except Exception as e:
            return {'error': f"Prediction error: {str(e)}"}
    
    def predict_batch(self, students_df: pd.DataFrame) -> pd.DataFrame:
        """
        Make predictions for multiple students
        
        Args:
            students_df: DataFrame with student data
            
        Returns:
            DataFrame with predictions added
        """
        results = []
        
        for idx, row in students_df.iterrows():
            # Convert row to dictionary
            student_data = {feat: row[feat] for feat in self.feature_names}
            
            # Make prediction
            result = self.predict_single(student_data)
            
            # Add to results
            result_row = {
                'index': idx + 1,
                'student_id': row.get('student_id', f'STD{idx+1:03d}'),
                'name': row.get('name', f'Student {idx+1}'),
                **result
            }
            results.append(result_row)
        
        return pd.DataFrame(results)
    
    def get_risk_factors(self, student_data: Dict) -> List[str]:
        """
        Identify key risk factors for a student
        
        Args:
            student_data: Dictionary with student features
            
        Returns:
            List of identified risk factors
        """
        risk_factors = []
        
        # Academic performance
        if student_data.get('G1', 20) < 10:
            risk_factors.append(f"Low first period grade ({student_data['G1']}/20)")
        
        if student_data.get('G2', 20) < 10:
            risk_factors.append(f"Low second period grade ({student_data['G2']}/20)")
        
        if student_data.get('failures', 0) > 0:
            risk_factors.append(f"{student_data['failures']} past failure(s)")
        
        # Attendance
        if student_data.get('absences', 0) > 10:
            risk_factors.append(f"High absences ({student_data['absences']})")
        
        # Study habits
        if student_data.get('studytime', 4) == 1:
            risk_factors.append("Very low study time (<2 hours/week)")
        
        # Resources
        if str(student_data.get('internet', 'yes')).lower() in ['no', 'n', '0', 'false']:
            risk_factors.append("No internet access at home")
        
        if str(student_data.get('schoolsup', 'no')).lower() in ['no', 'n', '0', 'false']:
            risk_factors.append("No extra educational support")
        
        # Socioeconomic
        if student_data.get('Medu', 4) == 0:
            risk_factors.append("Mother has no formal education")
        
        if student_data.get('Fedu', 4) == 0:
            risk_factors.append("Father has no formal education")
        
        return risk_factors
    
    def get_recommendations(self, prediction_result: Dict, student_data: Dict) -> Dict:
        """
        Generate recommendations based on prediction
        
        Args:
            prediction_result: Dictionary with prediction results
            student_data: Dictionary with student features
            
        Returns:
            Dictionary with recommendations
        """
        if prediction_result.get('error'):
            return {'error': prediction_result['error']}
        
        is_at_risk = prediction_result['prediction'] == 'At-Risk'
        risk_probability = prediction_result['risk_probability']
        
        recommendations = {
            'priority': 'High' if risk_probability > 80 else 'Medium' if risk_probability > 50 else 'Low',
            'actions': [],
            'risk_factors': self.get_risk_factors(student_data),
            'timeline': 'Immediate' if risk_probability > 80 else 'Within 1 week' if risk_probability > 50 else 'Monitor'
        }
        
        if is_at_risk:
            # High priority actions
            if risk_probability > 70:
                recommendations['actions'].extend([
                    "Schedule urgent meeting with student and parents/guardians",
                    "Implement immediate academic intervention plan",
                    "Assign dedicated mentor or tutor",
                    "Monitor attendance daily"
                ])
            
            # Academic support
            if student_data.get('G1', 20) < 10 or student_data.get('G2', 20) < 10:
                recommendations['actions'].append("Provide subject-specific tutoring")
            
            # Attendance issues
            if student_data.get('absences', 0) > 10:
                recommendations['actions'].extend([
                    "Investigate reasons for absences",
                    "Implement attendance improvement plan"
                ])
            
            # Study habits
            if student_data.get('studytime', 4) == 1:
                recommendations['actions'].extend([
                    "Teach study skills and time management",
                    "Create structured study schedule"
                ])
            
            # Resources
            if str(student_data.get('internet', 'yes')).lower() in ['no', 'n', '0']:
                recommendations['actions'].append("Provide access to school computer lab/resources")
            
        else:
            # For safe students
            recommendations['actions'] = [
                "Continue current support level",
                "Monitor for any changes in performance",
                "Recognize and encourage good work",
                "Maintain open communication"
            ]
        
        return recommendations


def create_predictor(model, feature_names: List[str]) -> StudentPredictor:
    """
    Factory function to create a StudentPredictor instance
    
    Args:
        model: Trained scikit-learn model
        feature_names: List of feature names
        
    Returns:
        StudentPredictor instance
    """
    return StudentPredictor(model, feature_names)
