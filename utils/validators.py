# validators.py
# Input validation utilities for Student Risk Prediction System

from typing import Any, Dict, List, Tuple, Optional
import pandas as pd


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class InputValidator:
    """
    Validates user input for student risk prediction
    """
    
    # Define valid ranges and values
    FEATURE_RANGES = {
        'G1': (0, 20),
        'G2': (0, 20),
        'failures': (0, 4),
        'absences': (0, 100),
        'studytime': (1, 4),
        'age': (15, 25),
        'Medu': (0, 4),
        'Fedu': (0, 4),
    }
    
    CATEGORICAL_VALUES = {
        'sex': ['M', 'F', 'MALE', 'FEMALE', 'm', 'f', 'male', 'female'],
        'address': ['U', 'R', 'URBAN', 'RURAL', 'u', 'r', 'urban', 'rural'],
        'schoolsup': ['yes', 'no', 'YES', 'NO', 'y', 'n', 'Y', 'N', '1', '0', 'true', 'false'],
        'internet': ['yes', 'no', 'YES', 'NO', 'y', 'n', 'Y', 'N', '1', '0', 'true', 'false'],
    }
    
    FEATURE_NAMES = {
        'G1': 'First period grade',
        'G2': 'Second period grade',
        'failures': 'Number of past failures',
        'absences': 'Number of absences',
        'studytime': 'Weekly study time',
        'age': 'Student age',
        'sex': 'Gender',
        'address': 'Address type',
        'Medu': "Mother's education level",
        'Fedu': "Father's education level",
        'schoolsup': 'Extra educational support',
        'internet': 'Internet access at home',
    }
    
    @classmethod
    def validate_numeric_field(cls, field_name: str, value: Any) -> Tuple[bool, Optional[str]]:
        """
        Validate a numeric field
        
        Args:
            field_name: Name of the field
            value: Value to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if field_name not in cls.FEATURE_RANGES:
            return False, f"Unknown field: {field_name}"
        
        min_val, max_val = cls.FEATURE_RANGES[field_name]
        friendly_name = cls.FEATURE_NAMES.get(field_name, field_name)
        
        # Check if value can be converted to number
        try:
            num_value = float(value)
        except (ValueError, TypeError):
            return False, f"{friendly_name} must be a valid number"
        
        # Check range
        if num_value < min_val:
            return False, f"{friendly_name} must be at least {min_val}"
        
        if num_value > max_val:
            return False, f"{friendly_name} cannot exceed {max_val}"
        
        # Check if should be integer
        if field_name in ['failures', 'absences', 'age', 'Medu', 'Fedu', 'studytime']:
            if num_value != int(num_value):
                return False, f"{friendly_name} must be a whole number"
        
        return True, None
    
    @classmethod
    def validate_categorical_field(cls, field_name: str, value: Any) -> Tuple[bool, Optional[str]]:
        """
        Validate a categorical field
        
        Args:
            field_name: Name of the field
            value: Value to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if field_name not in cls.CATEGORICAL_VALUES:
            return False, f"Unknown field: {field_name}"
        
        valid_values = cls.CATEGORICAL_VALUES[field_name]
        friendly_name = cls.FEATURE_NAMES.get(field_name, field_name)
        
        str_value = str(value).strip()
        
        if str_value not in valid_values:
            # Get expected values (simplified)
            if field_name == 'sex':
                expected = "M or F"
            elif field_name == 'address':
                expected = "U (Urban) or R (Rural)"
            else:
                expected = "yes or no"
            
            return False, f"{friendly_name} must be {expected}"
        
        return True, None
    
    @classmethod
    def validate_student_data(cls, data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate complete student data
        
        Args:
            data: Dictionary with student features
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        required_fields = list(cls.FEATURE_RANGES.keys()) + list(cls.CATEGORICAL_VALUES.keys())
        
        # Check for missing fields
        for field in required_fields:
            if field not in data or data[field] is None or str(data[field]).strip() == '':
                friendly_name = cls.FEATURE_NAMES.get(field, field)
                errors.append(f"{friendly_name} is required")
        
        # Validate numeric fields
        for field in cls.FEATURE_RANGES.keys():
            if field in data and data[field] is not None:
                is_valid, error_msg = cls.validate_numeric_field(field, data[field])
                if not is_valid:
                    errors.append(error_msg)
        
        # Validate categorical fields
        for field in cls.CATEGORICAL_VALUES.keys():
            if field in data and data[field] is not None:
                is_valid, error_msg = cls.validate_categorical_field(field, data[field])
                if not is_valid:
                    errors.append(error_msg)
        
        return len(errors) == 0, errors
    
    @classmethod
    def validate_csv_file(cls, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate uploaded CSV file
        
        Args:
            df: Pandas DataFrame from CSV
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        required_columns = list(cls.FEATURE_RANGES.keys()) + list(cls.CATEGORICAL_VALUES.keys())
        
        # Check for required columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")
            return False, errors
        
        # Validate data types and ranges
        for idx, row in df.iterrows():
            row_errors = []
            
            # Validate numeric fields
            for field in cls.FEATURE_RANGES.keys():
                if field in row:
                    is_valid, error_msg = cls.validate_numeric_field(field, row[field])
                    if not is_valid:
                        row_errors.append(error_msg)
            
            # Validate categorical fields
            for field in cls.CATEGORICAL_VALUES.keys():
                if field in row:
                    is_valid, error_msg = cls.validate_categorical_field(field, row[field])
                    if not is_valid:
                        row_errors.append(error_msg)
            
            if row_errors:
                student_id = row.get('student_id', idx + 1)
                errors.append(f"Row {idx + 1} (Student {student_id}): {'; '.join(row_errors)}")
        
        return len(errors) == 0, errors
    
    @classmethod
    def sanitize_input(cls, data: Dict) -> Dict:
        """
        Clean and sanitize input data
        
        Args:
            data: Dictionary with student features
            
        Returns:
            Sanitized dictionary
        """
        sanitized = {}
        
        # Numeric fields - convert to appropriate type
        for field in cls.FEATURE_RANGES.keys():
            if field in data:
                try:
                    if field in ['failures', 'absences', 'age', 'Medu', 'Fedu', 'studytime']:
                        sanitized[field] = int(float(data[field]))
                    else:
                        sanitized[field] = float(data[field])
                except (ValueError, TypeError):
                    sanitized[field] = data[field]  # Keep original if can't convert
        
        # Categorical fields - normalize
        for field in cls.CATEGORICAL_VALUES.keys():
            if field in data:
                value = str(data[field]).strip()
                
                # Normalize to standard format
                if field == 'sex':
                    sanitized[field] = 'M' if value.upper() in ['M', 'MALE'] else 'F'
                elif field == 'address':
                    sanitized[field] = 'U' if value.upper() in ['U', 'URBAN'] else 'R'
                elif field in ['schoolsup', 'internet']:
                    sanitized[field] = 'yes' if value.lower() in ['yes', 'y', '1', 'true'] else 'no'
        
        return sanitized
    
    @classmethod
    def get_validation_rules(cls) -> Dict:
        """
        Get validation rules for frontend
        
        Returns:
            Dictionary with validation rules
        """
        return {
            'numeric_ranges': cls.FEATURE_RANGES,
            'categorical_values': cls.CATEGORICAL_VALUES,
            'feature_names': cls.FEATURE_NAMES
        }


class FileValidator:
    """
    Validates uploaded files
    """
    
    ALLOWED_EXTENSIONS = {'csv'}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    MAX_ROWS = 1000  # Maximum number of students
    
    @classmethod
    def validate_file_extension(cls, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Check if file has allowed extension
        
        Args:
            filename: Name of the file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if '.' not in filename:
            return False, "File must have an extension"
        
        extension = filename.rsplit('.', 1)[1].lower()
        
        if extension not in cls.ALLOWED_EXTENSIONS:
            return False, f"Only CSV files are allowed (got .{extension})"
        
        return True, None
    
    @classmethod
    def validate_file_size(cls, file_size: int) -> Tuple[bool, Optional[str]]:
        """
        Check if file size is within limits
        
        Args:
            file_size: Size of file in bytes
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if file_size > cls.MAX_FILE_SIZE:
            max_mb = cls.MAX_FILE_SIZE / (1024 * 1024)
            return False, f"File size must not exceed {max_mb:.1f}MB"
        
        if file_size == 0:
            return False, "File is empty"
        
        return True, None
    
    @classmethod
    def validate_csv_structure(cls, df: pd.DataFrame) -> Tuple[bool, Optional[str]]:
        """
        Validate CSV structure
        
        Args:
            df: Pandas DataFrame
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(df) == 0:
            return False, "CSV file is empty"
        
        if len(df) > cls.MAX_ROWS:
            return False, f"Too many rows. Maximum is {cls.MAX_ROWS} students"
        
        return True, None


def validate_form_data(form_data: Dict) -> Dict:
    """
    Validate form data and return sanitized version or errors
    
    Args:
        form_data: Form data dictionary
        
    Returns:
        Dictionary with 'valid', 'data', and 'errors' keys
    """
    is_valid, errors = InputValidator.validate_student_data(form_data)
    
    if is_valid:
        sanitized_data = InputValidator.sanitize_input(form_data)
        return {
            'valid': True,
            'data': sanitized_data,
            'errors': []
        }
    else:
        return {
            'valid': False,
            'data': None,
            'errors': errors
        }


def validate_csv_upload(file) -> Dict:
    """
    Validate uploaded CSV file
    
    Args:
        file: Uploaded file object
        
    Returns:
        Dictionary with validation results
    """
    # Check filename
    is_valid, error_msg = FileValidator.validate_file_extension(file.filename)
    if not is_valid:
        return {'valid': False, 'errors': [error_msg]}
    
    # Check file size (if available)
    try:
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        is_valid, error_msg = FileValidator.validate_file_size(file_size)
        if not is_valid:
            return {'valid': False, 'errors': [error_msg]}
    except:
        pass  # Skip size check if not available
    
    # Try to read CSV
    try:
        df = pd.read_csv(file)
    except Exception as e:
        return {'valid': False, 'errors': [f"Error reading CSV file: {str(e)}"]}
    
    # Validate structure
    is_valid, error_msg = FileValidator.validate_csv_structure(df)
    if not is_valid:
        return {'valid': False, 'errors': [error_msg]}
    
    # Validate data
    is_valid, errors = InputValidator.validate_csv_file(df)
    
    if is_valid:
        return {
            'valid': True,
            'data': df,
            'errors': []
        }
    else:
        return {
            'valid': False,
            'data': None,
            'errors': errors
        }
