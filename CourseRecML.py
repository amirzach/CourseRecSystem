import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Function to convert letter grades to numeric values
def grade_to_numeric(grade):
    grade_map = {'A+': 4.3, 'A': 4, 'A-': 3.7, 'B+': 3.3, 'B': 3, 'B-': 2.7, 'C': 2, 'D': 1, 'E': 0.5, 'F': 0}
    return grade_map.get(grade, 0)  # Default to 0 if grade not found

# Load the Excel file
file_path = r'C:\Users\User\spmresultsdataset_fyphelper.xlsx'
data = pd.read_excel(file_path)

# Clean column names
data.columns = data.columns.str.strip().str.replace('\n', '').str.upper()

# Drop irrelevant columns
columns_to_drop = ['ANGKA GILIRAN']
data_cleaned = data.drop(columns=columns_to_drop, errors='ignore')

# Ensure the name column exists (use 'NAMA' if it is in the dataset)
data_cleaned['NAME'] = data_cleaned['NAMA']

# Convert grades to numeric values
for col in ['MATEMATIK', 'MATEMATIK TAMBAHAN', 'FIZIK', 'BIOLOGI', 'KIMIA', 
            'BAHASA MALAYSIA', 'BAHASA INGGERIS', 'PENDIDIKAN SENI VISUAL', 
            'EKONOMI', 'PERNIAGAAN', 'PRINSIP PERAKAUNAN', 'TASAWWUR ISLAM', 
            'PENDIDIKAN ISLAM', 'SEJARAH', 'MORAL', 'SAINS']:
    data_cleaned[col] = data_cleaned[col].apply(grade_to_numeric)

# Handle missing or invalid data (if any)
data_cleaned = data_cleaned.fillna(0)

# Define the target variable (Recommended Course)
def assign_course(row):
    recommended_courses = []
    if row['MATEMATIK'] >= 3.7 and row['MATEMATIK TAMBAHAN'] >= 3.7 and row['FIZIK'] >= 3:
        recommended_courses.append('Engineering')
    if row['BIOLOGI'] >= 3.7 and row['FIZIK'] >= 3 and row['KIMIA'] >= 3:
        recommended_courses.append('Science')
    if row['BIOLOGI'] >= 3.5 and row['KIMIA'] >= 3.5:
        recommended_courses.append('Biotechnology')
    if row['BIOLOGI'] >= 3 and row['KIMIA'] >= 3 and row['PENDIDIKAN SENI VISUAL'] >= 3:
        recommended_courses.append('Food Technology')
    if row['PENDIDIKAN SENI VISUAL'] >= 3.7 and row['BAHASA INGGERIS'] >= 3:
        recommended_courses.append('Fine Arts and Design')
    if row['EKONOMI'] >= 3.5 or row['PERNIAGAAN'] >= 3.5 or row['PRINSIP PERAKAUNAN'] >= 3.5:
        recommended_courses.append('Commerce')
    if row['MATEMATIK'] >= 3.5 and row['BAHASA INGGERIS'] >= 3:
        recommended_courses.append('Information Technology')
    if row['SEJARAH'] >= 3 and row['BAHASA INGGERIS'] >= 3:
        recommended_courses.append('Law and Policing')
    if row['PENDIDIKAN ISLAM'] >= 3.5 or row['TASAWWUR ISLAM'] >= 3.5:
        recommended_courses.append('Islamic Studies and TESL')
    if row['BAHASA MALAYSIA'] >= 3 and row['BAHASA INGGERIS'] >= 3 and row['PENDIDIKAN SENI VISUAL'] >= 3:
        recommended_courses.append('Arts and Media')
    if row['BIOLOGI'] >= 3 and row['MORAL'] >= 3:
        recommended_courses.append('Psychology and Health')
    if row['BAHASA INGGERIS'] >= 3.5 and row['PENDIDIKAN ISLAM'] >= 3.5:
        recommended_courses.append('Education')
    if row['PERNIAGAAN'] >= 3.5 and row['SEJARAH'] >= 3.5:
        recommended_courses.append('Travel and Hospitality')
    
    # If no courses match, recommend 'General'
    if not recommended_courses:
        recommended_courses.append('General')
    
    return recommended_courses

# Apply the manual rule to assign courses
data_cleaned['RECOMMENDED_COURSES'] = data_cleaned.apply(assign_course, axis=1)

# Encode target variable (Recommended Course)
label_encoder = LabelEncoder()
# Flatten the recommended courses list for encoding
flattened_courses = [course for courses in data_cleaned['RECOMMENDED_COURSES'] for course in courses]
unique_courses = list(set(flattened_courses))

# Assign numeric labels for each unique course
course_labels = {course: idx for idx, course in enumerate(unique_courses)}

# Create a new column with numeric labels for the recommended courses
data_cleaned['COURSE'] = data_cleaned['RECOMMENDED_COURSES'].apply(lambda x: [course_labels[course] for course in x])

# Split the data into features (X) and target (y)
X = data_cleaned.drop(columns=['COURSE', 'NAME', 'RECOMMENDED_COURSES'], errors='ignore')  # Drop only existing columns
y = data_cleaned['COURSE'].apply(lambda x: x[0] if len(x) > 0 else 0)  # Simplify to a single course for classification

# Ensure all columns in X are numeric
X = X.apply(pd.to_numeric, errors='coerce')  # This will turn any invalid data into NaN

# Handle any NaN values that might have been introduced
X = X.fillna(0)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a Decision Tree classifier
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)

# Predict the course recommendations
y_pred = dt_model.predict(X_test)

# Evaluate the model accuracy
accuracy = accuracy_score(y_test, y_pred)

# Print accuracy as percentage
print(f'Accuracy: {accuracy * 100:.2f}%')

# First cycle: Recommend multiple courses for all students
data_cleaned['Recommended Courses'] = data_cleaned['RECOMMENDED_COURSES'].apply(lambda x: ', '.join(x))

# Save the multiple course recommendations to a new Excel file
output_path_multiple = r'C:\Users\User\recommended_courses_ml_multiple.xlsx'
data_cleaned.to_excel(output_path_multiple, index=False)

print(f"Multiple course recommendations saved to {output_path_multiple}")