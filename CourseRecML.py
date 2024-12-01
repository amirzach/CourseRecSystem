import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Function to convert letter grades to numeric values
def grade_to_numeric(grade):
    grade_map = {'A': 4, 'A-': 3.7, 'B+': 3.3, 'B': 3, 'B-': 2.7, 'C+': 2.3, 'C': 2, 'C-': 1.7, 'D': 1, 'E': 0}
    return grade_map.get(grade, 0)  # Default to 0 if grade not found

# Load the Excel file
file_path = r'C:\Users\User\spmresultsdataset_fyphelper.xlsx'
data = pd.read_excel(file_path)

# Clean column names
data.columns = data.columns.str.strip().str.replace('\n', '').str.upper()

# Drop irrelevant columns
columns_to_drop = ['NAMA', 'ANGKA GILIRAN']
data_cleaned = data.drop(columns=columns_to_drop, errors='ignore')

# Convert grades to numeric values
for col in ['MATEMATIK', 'MATEMATIK TAMBAHAN', 'FIZIK', 'BIOLOGI', 'KIMIA', 
            'BAHASA MALAYSIA', 'BAHASA INGGERIS', 'PENDIDIKAN SENI VISUAL', 
            'EKONOMI', 'PERNIAGAAN', 'PRINSIP PERAKAUNAN', 'TASAWWUR ISLAM', 
            'PENDIDIKAN ISLAM', 'SEJARAH', 'MORAL', 'SAINS']:
    data_cleaned[col] = data_cleaned[col].apply(grade_to_numeric)

# Check for any non-numeric values in the dataset
for col in data_cleaned.columns:
    if data_cleaned[col].dtype == 'object':
        print(f"Non-numeric values in column {col}:")
        print(data_cleaned[col].unique())

# Handle missing or invalid data (if any)
data_cleaned = data_cleaned.fillna(0)

# Define the target variable (Recommended Course)
# Example of how to map the courses (use rules based on the grades)
def assign_course(row):
    if row['MATEMATIK'] >= 3.7 and row['MATEMATIK TAMBAHAN'] >= 3.7 and row['FIZIK'] >= 3:
        return 'Engineering'
    elif row['BIOLOGI'] >= 3.7 and row['FIZIK'] >= 3 and row['KIMIA'] >= 3:
        return 'Science'
    elif row['BAHASA MALAYSIA'] >= 3 and row['BAHASA INGGERIS'] >= 3 and row['PENDIDIKAN SENI VISUAL'] >= 3:
        return 'Arts'
    elif row['EKONOMI'] >= 3 or row['PERNIAGAAN'] >= 3 or row['PRINSIP PERAKAUNAN'] >= 3:
        return 'Commerce'
    else:
        return 'General'

# Apply the manual rule to assign courses
data_cleaned['COURSE'] = data_cleaned.apply(assign_course, axis=1)

# Encode target variable (Recommended Course)
label_encoder = LabelEncoder()
data_cleaned['COURSE'] = label_encoder.fit_transform(data_cleaned['COURSE'])

# Split the data into features (X) and target (y)
X = data_cleaned.drop(columns=['COURSE'])
y = data_cleaned['COURSE']

# Ensure all columns in X are numeric
X = X.apply(pd.to_numeric, errors='coerce')  # This will turn any invalid data into NaN

# Handle any NaN values that might have been introduced
X = X.fillna(0)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a Random Forest classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict the course recommendations
y_pred = model.predict(X_test)

# Evaluate the model accuracy
accuracy = accuracy_score(y_test, y_pred)

# Print accuracy as percentage
print(f'Accuracy: {accuracy * 100:.2f}%')

# Apply the model to the entire dataset (for new predictions)
data_cleaned['Recommended Course'] = label_encoder.inverse_transform(model.predict(X))

# Save the result to a new Excel file
output_path = r'C:\Users\User\recommended_courses_ml.xlsx'
data_cleaned.to_excel(output_path, index=False)

print(f"Course recommendations saved to {output_path}")
