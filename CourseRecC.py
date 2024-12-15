import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load data from a spreadsheet
def load_data(filepath):
    df = pd.read_excel(filepath)
    print("Columns in the dataset:", df.columns)
    return df

# Train the Decision Tree Model
def train_decision_tree(X_train, y_train):
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    return model

# Content-Based Filtering: Compute similarity scores
def content_based_filtering(df, user_answers):
    dataset_features = df.drop(columns=["Course"])
    similarity_scores = cosine_similarity([user_answers], dataset_features)
    most_similar_index = np.argmax(similarity_scores)
    return df.iloc[most_similar_index]["Course"]

# Get user input
def get_user_input():
    print("Please answer the following questions on a scale of 1 to 5 where applicable:\n")
    
    questions = [
        "1. Do you consider yourself more (1=creative, 2=analytical, or 3=practical)?",
        "2. Which set of skills or interests best describes you?\n"
        "   1. Problem-solving, logical thinking, and an interest in how things work.\n"
        "   2. Curiosity about nature, scientific research, and exploring how the world works.\n"
        "   3. Interest in biology, innovation, and working on solutions to health or environmental issues.\n"
        "   4. Creativity in designing or making things, especially in food or other practical applications.\n"
        "   5. Artistic talent, creativity, and a passion for visual expression.\n"
        "   6. Business-minded, with an interest in economics, finance, or managing projects.\n"
        "   7. Interest in technology, computers, and solving problems using logical approaches.\n"
        "   8. Passion for history, law, or making a difference in society through governance or public service.\n"
        "   9. Interest in teaching, religious studies, or exploring cultural traditions.\n"
        "  10. Communication skills, creativity, and a passion for media, storytelling, or the arts.\n"
        "  11. Interest in understanding human behavior, empathy, and helping others.\n"
        "  12. Enjoy working with people, sharing knowledge, and guiding others.\n"
        "  13. Love for exploring new places, cultures, and organizing travel experiences.\n"
        "   (Enter the number corresponding to your choice): ",
        "3. How do you approach solving problems: (1=step-by-step or 2=intuitively)?",
        "4. Are you more comfortable working with (1=data, 2=people, or 3=ideas)?",
        "5. How would you describe your learning style: (1=visual, 2=auditory, 3=reading/writing, or 4=kinesthetic)?",
        "6. How confident are you in your mathematical skills? (1 = Not confident, 5 = Very confident)",
        "7. How would you rate your ability to understand and apply scientific concepts like biology, physics, or chemistry? (1 = Poor, 5 = Excellent)",
        "8. How proficient are you in solving additional mathematics problems? (1 = Not proficient, 5 = Highly proficient)",
        "9. How would you rate your artistic or visual design abilities? (1 = Very weak, 5 = Very strong)",
        "10. How comfortable are you working on experiments or lab-based tasks? (1 = Very uncomfortable, 5 = Very comfortable)",
        "11. How would you rate your understanding of economics, accounting, or business concepts? (1 = Very weak, 5 = Very strong)",
        "12. How confident are you in your command of the English language, both written and spoken? (1 = Not confident, 5 = Very confident)",
        "13. How skilled are you at analyzing historical or legal concepts? (1 = Not skilled, 5 = Highly skilled)",
        "14. How strong is your grasp of Islamic Studies or moral concepts? (1 = Very weak, 5 = Very strong)",
        "15. How well do you communicate in Bahasa Malaysia? (1 = Poorly, 5 = Fluently)",
        "16. How much do you enjoy solving complex problems? (1 = Not at all, 5 = Very much)",
        "17. Do you prefer hands-on, practical work or theoretical study? (1 = Entirely theoretical, 5 = Entirely practical)",
        "18. How creative are you in coming up with new ideas or designs? (1 = Not creative, 5 = Highly creative)",
        "19. How comfortable are you working with technology and learning new software tools? (1 = Not comfortable, 5 = Very comfortable)",
        "20. Do you enjoy working with numbers and financial data? (1 = Not at all, 5 = Very much)",
        "21. How much do you enjoy exploring human behavior or psychological concepts? (1 = Not at all, 5 = Very much)",
        "22. Do you enjoy planning trips, learning about different cultures, or engaging in hospitality-related tasks? (1 = Not at all, 5 = Very much)",
        "23. How confident are you in your ability to lead and manage projects or teams? (1 = Not confident, 5 = Very confident)",
        "24. Do you prefer working in structured environments or dynamic, creative spaces? (1 = Entirely structured, 5 = Entirely dynamic)",
        "25. How interested are you in contributing to society through teaching or educational programs? (1 = Not at all, 5 = Very interested)"
    ]

    user_input = []
    for idx, question in enumerate(questions):
        while True:
            try:
                answer = int(input(f"{question}\nYour answer: "))
                
                # Custom range validation
                if idx == 1:  # Question 2 allows 1-13
                    if 1 <= answer <= 13:
                        user_input.append(answer)
                        break
                elif 1 <= answer <= 5:  # Most questions allow 1-5
                    user_input.append(answer)
                    break
                elif idx in [0, 2, 3]:  # Questions with a smaller range
                    if 1 <= answer <= 3:
                        user_input.append(answer)
                        break
                else:
                    print("Please enter a valid number within the range.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    return user_input

# Main Function
def main():
    # Load data from a spreadsheet
    filepath = r'C:\Users\User\QuestionnaireResultsHelper.xlsx'
    df = load_data(filepath)
    
    # Prepare the dataset
    X = df.drop(columns=["Course"])
    y = df["Course"]
    
    # Encode the target labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Split the dataset into training and testing subsets
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    # Train the Decision Tree
    model = train_decision_tree(X_train, y_train)
    
    # Get user input
    user_answers = get_user_input()
    
    # Convert user input to DataFrame with matching feature names
    user_answers_df = pd.DataFrame([user_answers], columns=X.columns)
    
    # Decision Tree Prediction
    prediction = model.predict(user_answers_df)
    recommended_course_dt = le.inverse_transform(prediction)[0]
    
    # Content-Based Filtering
    recommended_course_cb = content_based_filtering(df, user_answers)
    
    # Combine and Display Results
    print("\nRecommendation Results:")
    print(f"Decision Tree AI suggests: {recommended_course_dt}")
    print(f"Content-Based Filtering suggests: {recommended_course_cb}")
    if recommended_course_dt == recommended_course_cb:
        print(f"Final Recommendation: {recommended_course_dt}")
    else:
        print(f"Combined Recommendation: {recommended_course_dt} (primary), {recommended_course_cb} (secondary)")
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nDecision Tree Model Accuracy on Test Data: {accuracy * 100:.2f}%")

# Run the program
if __name__ == "__main__":
    main()


