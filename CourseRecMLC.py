import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import numpy as np

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
    if row['MATEMATIK'] >= 3.7 and row['MATEMATIK TAMBAHAN'] >= 3.7 and row['FIZIK'] >= 3:
        return 'Engineering'
    elif row['BIOLOGI'] >= 3.7 and row['FIZIK'] >= 3 and row['KIMIA'] >= 3:
        return 'Science'
    elif row['BIOLOGI'] >= 3.5 and row['KIMIA'] >= 3.5:
        return 'Biotechnology'
    elif row['BIOLOGI'] >= 3 and row['KIMIA'] >= 3 and row['PENDIDIKAN SENI VISUAL'] >= 3:
        return 'Food Technology'
    elif row['PENDIDIKAN SENI VISUAL'] >= 3.7 and row['BAHASA INGGERIS'] >= 3:
        return 'Fine Arts and Design'
    elif row['EKONOMI'] >= 3.5 or row['PERNIAGAAN'] >= 3.5 or row['PRINSIP PERAKAUNAN'] >= 3.5:
        return 'Commerce'
    elif row['MATEMATIK'] >= 3.5 and row['BAHASA INGGERIS'] >= 3:
        return 'Information Technology'
    elif row['SEJARAH'] >= 3 and row['BAHASA INGGERIS'] >= 3:
        return 'Law and Policing'
    elif row['PENDIDIKAN ISLAM'] >= 3.5 or row['TASAWWUR ISLAM'] >= 3.5:
        return 'Islamic Studies and TESL'
    elif row['BAHASA MALAYSIA'] >= 3 and row['BAHASA INGGERIS'] >= 3 and row['PENDIDIKAN SENI VISUAL'] >= 3:
        return 'Arts and Media'
    elif row['BIOLOGI'] >= 3 and row['MORAL'] >= 3:
        return 'Psychology and Health'
    elif row['BAHASA INGGERIS'] >= 3.5 and row['PENDIDIKAN ISLAM'] >= 3.5:
        return 'Education'
    elif row['PERNIAGAAN'] >= 3.5 and row['SEJARAH'] >= 3.5:
        return 'Travel and Hospitality'
    else:
        return 'General'

# Apply the manual rule to assign courses
data_cleaned['COURSE'] = data_cleaned.apply(assign_course, axis=1)

# Encode target variable (Recommended Course)
label_encoder = LabelEncoder()
data_cleaned['COURSE'] = label_encoder.fit_transform(data_cleaned['COURSE'])

# Split the data into features (X) and target (y)
X = data_cleaned.drop(columns=['COURSE', 'NAME'])
y = data_cleaned['COURSE']

# Ensure all columns in X are numeric
X = X.apply(pd.to_numeric, errors='coerce')  # This will turn any invalid data into NaN

# Handle any NaN values that might have been introduced
X = X.fillna(0)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a Decision Tree classifier
model = DecisionTreeClassifier(random_state=42)
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

def get_user_preferences():
    print("Please answer the following questions to help modify the course recommendation:")
    
    # Example questions based on user's preferences
    preferences = {
        'Mathematics': int(input("On a scale of 1-5, how confident are you in Mathematics? (1 = Not confident, 5 = Very confident): ")),
        'Science': int(input("On a scale of 1-5, how confident are you in Science subjects? (1 = Not confident, 5 = Very confident): ")),
        'Arts': int(input("On a scale of 1-5, how confident are you in Arts subjects? (1 = Not confident, 5 = Very confident): ")),
        'Business': int(input("On a scale of 1-5, how confident are you in Business-related subjects? (1 = Not confident, 5 = Very confident): ")),
        'Technology': int(input("On a scale of 1-5, how interested are you in Technology-related fields? (1 = Not interested, 5 = Very interested): ")),
        'Health': int(input("On a scale of 1-5, how interested are you in Health-related fields? (1 = Not interested, 5 = Very interested): ")),
        'Design': int(input("On a scale of 1-5, how interested are you in Design or Creative Arts? (1 = Not interested, 5 = Very interested): ")),
        'Learning Style': input("Do you prefer hands-on practical learning? (Yes/No): ").lower() == 'yes'
    }
    
    return preferences

# Ask the user for the name of the student to modify
student_name = input("Enter the name of the student whose course recommendation you want to modify: ")

# Find the row corresponding to the student
student_row = data_cleaned[data_cleaned['NAME'].str.lower() == student_name.lower()]

if student_row.empty:
    print(f"No student found with the name {student_name}. Please check the spelling.")
else:
    # Get user preferences for content-based filtering
    user_preferences = get_user_preferences()

    # Create a new dataframe for the user's preferences
    user_df = pd.DataFrame([user_preferences])

    # Define the feature columns for the dataset (expanded to include new areas)
    feature_columns = [
        'MATEMATIK', 'MATEMATIK TAMBAHAN', 'FIZIK', 'BIOLOGI', 'KIMIA', 
        'BAHASA MALAYSIA', 'BAHASA INGGERIS', 'PENDIDIKAN SENI VISUAL', 
        'EKONOMI', 'PERNIAGAAN', 'PRINSIP PERAKAUNAN', 'TASAWWUR ISLAM', 
        'PENDIDIKAN ISLAM', 'SEJARAH', 'MORAL', 'SAINS', 
        'Learning Style', 'Technology', 'Health', 'Design'
    ]

    # Initialize missing columns with default values
    for col in feature_columns:
        if col not in user_df.columns:
            user_df[col] = 0  # Default to 0 if the column is missing

    # Add the user's preferences into the appropriate columns
    user_df['MATEMATIK'] = user_preferences.get('Mathematics', 0)
    user_df['BIOLOGI'] = user_preferences.get('Science', 0)
    user_df['PENDIDIKAN SENI VISUAL'] = user_preferences.get('Arts', 0)
    user_df['EKONOMI'] = user_preferences.get('Business', 0)
    user_df['Technology'] = user_preferences.get('Technology', 0)
    user_df['Health'] = user_preferences.get('Health', 0)
    user_df['Design'] = user_preferences.get('Design', 0)
    user_df['Learning Style'] = 1 if user_preferences.get('Learning Style', False) else 0

    # Ensure that user_df has the same feature order as X
    user_df = user_df[feature_columns]

    # Calculate cosine similarity between user preferences and the dataset
    similarity_scores = cosine_similarity(user_df, X)

    # Get the index of the most similar row (the best course match)
    best_match_index = np.argmax(similarity_scores)

    # Adjust the course recommendation based on the most similar match
    recommended_course_based_on_content = label_encoder.inverse_transform([y.iloc[best_match_index]])

    print(f"Based on the student's preferences, we recommend: {recommended_course_based_on_content[0]}")

    # Modify the student's course recommendation in the dataset
    data_cleaned.loc[data_cleaned['NAME'].str.lower() == student_name.lower(), 'Modified Recommended Course'] = recommended_course_based_on_content[0]

    # Save the result to a new Excel file
    modified_output_path = r'C:\Users\User\modified_recommended_courses.xlsx'
    data_cleaned.to_excel(modified_output_path, index=False)

    print(f"Modified course recommendations saved to {modified_output_path}")


