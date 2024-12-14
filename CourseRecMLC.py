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

# Function to select the user to modify before proceeding
def select_user(data):
    print("Please select the user whose course recommendations will be modified:")
    print("Available users:")
    for idx, name in enumerate(data['NAME'].unique(), 1):
        print(f"{idx}. {name}")
    
    user_choice = int(input("Enter the number corresponding to the user: "))
    
    selected_user_name = data['NAME'].unique()[user_choice - 1]
    selected_user_data = data[data['NAME'] == selected_user_name]
    
    return selected_user_data, selected_user_name

# Function to ask users refined questions and calculate a score for courses
def calculate_course_scores(user_preferences, course_profiles):
    scores = {}
    for course, profile in course_profiles.items():
        score = sum([profile[feature] * user_preferences.get(feature, 0) for feature in profile])
        scores[course] = score
    return scores

def refine_courses(user_preferences, recommended_courses, course_profiles):
    # Calculate course scores
    course_scores = calculate_course_scores(user_preferences, course_profiles)
    
    # Validate recommended courses against available course profiles
    valid_courses = [course for course in recommended_courses if course in course_profiles]
    
    if not valid_courses:
        print("Error: None of the recommended courses have profiles in the system.")
        return None  # Exit or handle error appropriately
    
    # Filter scores for valid recommended courses only
    filtered_scores = {course: course_scores.get(course, 0) for course in valid_courses}
    
    # Sort courses by score (descending)
    sorted_courses = sorted(filtered_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Decision tree classifier for final decision
    # Generate sample decision tree input data
    X = np.array([[course_profiles[course][feature] for feature in user_preferences.keys()] for course in valid_courses])
    y = valid_courses
    decision_tree = DecisionTreeClassifier()
    decision_tree.fit(X, y)
    
    # Predict the most suitable course based on user preferences
    refined_course = decision_tree.predict([list(user_preferences.values())])[0]
    
    # If refined course is not in valid recommended courses, default to the top-scored course
    if refined_course not in valid_courses:
        refined_course = sorted_courses[0][0]
    
    return refined_course

# Example course profiles (features can include skills, interest, difficulty, etc.)
course_profiles = {
    "Engineering": {"math": 5, "science": 4, "creativity": 2, "teamwork": 3},
    "Science": {"math": 4, "science": 5, "creativity": 3, "teamwork": 2},
    "Fine Arts": {"math": 1, "science": 1, "creativity": 5, "teamwork": 4},
    "Law": {"math": 2, "science": 2, "creativity": 3, "teamwork": 5},
    "Psychology": {"math": 2, "science": 3, "creativity": 4, "teamwork": 5},
    "Hospitality": {"math": 1, "science": 2, "creativity": 4, "teamwork": 5}
}

# Refine course recommendations for a selected user
selected_user_data, selected_user_name = select_user(data_cleaned)

# Get the recommended courses for the selected user
recommended_courses_for_user = selected_user_data['RECOMMENDED_COURSES'].iloc[0]  # Assuming one row per user
print(f"Original course recommendations for {selected_user_name}: {', '.join(recommended_courses_for_user)}")

# Get user preferences (ask refined questions)
print("Answer the following questions to refine your preferences:")
user_preferences = {
    "math": int(input("Rate your interest in mathematics (1-5): ")),
    "science": int(input("Rate your interest in science (1-5): ")),
    "creativity": int(input("Rate your creativity level (1-5): ")),
    "teamwork": int(input("Rate your ability to work in teams (1-5): "))
}

# Refine the course recommendations using the decision tree
refined_course = refine_courses(user_preferences, recommended_courses_for_user, course_profiles)

# Output the refined course recommendation
print(f"Refined course recommendation for {selected_user_name}: {refined_course}")

# Update the user's refined course in the dataset
data_cleaned.loc[data_cleaned['NAME'] == selected_user_name, 'Refined Recommended Course'] = refined_course

# Save the updated recommendations to a new Excel file
output_path_refined = r'C:\Users\User\recommended_courses_ml_refined_updated.xlsx'
data_cleaned.to_excel(output_path_refined, index=False)

print(f"Refined course recommendations saved to {output_path_refined}")

