# Converts your original csv to the format needed for batch upload

import pandas as pd

print("CSV CONVERTER FOR BATCH UPLOAD")

# 1. Load your original file
print("\n1. Loading original CSV...")
df = pd.read_csv('student-mat.csv', sep=';')
print(f"   Loaded {len(df)} students")
print(f"   Original columns: {len(df.columns)}")

# 2. Select ONLY the 13 required columns
print("\n2. Selecting required 13 columns...")

required_columns = [
    'age', 'Medu', 'Fedu', 'studytime', 'failures', 'absences', 
    'G1', 'G2', 'sex', 'address', 'schoolsup', 'famsup', 'internet'
]

# Check if all required columns exist
missing = [col for col in required_columns if col not in df.columns]
if missing:
    print(f"   ❌ ERROR: Missing columns in your file: {missing}")
    exit()

# Select only required columns
df_batch = df[required_columns].copy()

print(f"   ✅ Selected columns: {list(df_batch.columns)}")
print(f"   ✅ Total: {len(df_batch.columns)} columns")

# 3. Add optional student_id for identification
print("\n3. Adding student IDs...")
df_batch.insert(0, 'student_id', [f'STD{i+1:03d}' for i in range(len(df_batch))])

# 4. Preview the data
print("\n4. Preview of converted data:")
print(df_batch.head(3))

# 5. Save to new CSV file
output_file = 'students_batch_upload.csv'
df_batch.to_csv(output_file, index=False)

print(f"\n✅✅✅ SUCCESS!")
print(f"\n📁 File saved as: {output_file}")
print(f"📊 Students: {len(df_batch)}")
print(f"📋 Columns: {len(df_batch.columns)}")
print(f"\n✅ This file is ready to upload to your batch interface!")

print("NEXT STEPS:")
print("1. Upload 'students_batch_upload.csv' to your Flask batch page")
print("2. It should work perfectly now!")