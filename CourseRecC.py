from sklearn.tree import DecisionTreeClassifier
import pandas as pd

# Extended dataset with features aligned to the questionnaire
data = {
    "Creative_Analytical_Practical": ["Creative", "Analytical", "Practical", "Analytical", "Creative", "Practical", "Analytical", "Creative", "Analytical", "Practical", "Creative", "Analytical", "Practical", "Creative", "Creative", "Practical", "Analytical", "Creative", "Practical", "Analytical"],
    "Skill_Interest_Set": ["Arts and Design", "Engineering or Technology", "Business", "Science", "Biotechnology", "Food Technology", "Fine Arts and Design", "Commerce", "Information Technology", "Law and Policing", "Islamic Studies and TESL", "Arts and Media", "Psychology and Health", "Education", "Travel and Hospitality", "General", "Engineering", "Science", "Biotechnology", "Food Technology"],
    "Problem_Solving_Approach": ["Intuitively", "Step-by-step", "Step-by-step", "Intuitively", "Step-by-step", "Step-by-step", "Intuitively", "Step-by-step", "Intuitively", "Step-by-step", "Step-by-step", "Intuitively", "Intuitively", "Step-by-step", "Step-by-step", "Intuitively", "Step-by-step", "Step-by-step", "Intuitively", "Step-by-step"],
    "Comfort_Working_With": ["Ideas", "Data", "People", "Data", "Ideas", "People", "Ideas", "People", "Data", "Ideas", "People", "Ideas", "Data", "People", "Ideas", "Data", "People", "Ideas", "People", "Data"],
    "Mathematical_Skills": [3, 5, 2, 4, 3, 5, 2, 4, 3, 5, 4, 2, 3, 4, 5, 4, 5, 3, 5, 4],
    "Scientific_Concepts": [3, 5, 1, 4, 5, 5, 3, 4, 3, 5, 4, 1, 3, 4, 5, 4, 4, 3, 5, 3],
    "Additional_Maths_Skills": [4, 5, 2, 3, 4, 5, 3, 2, 4, 5, 3, 2, 4, 5, 4, 3, 5, 4, 3, 5],
    "Artistic_Abilities": [5, 2, 1, 3, 5, 4, 5, 3, 2, 1, 2, 3, 5, 4, 3, 5, 3, 4, 2, 3],
    "Lab_Tasks_Comfort": [2, 5, 1, 4, 4, 3, 1, 5, 3, 4, 5, 2, 4, 3, 5, 4, 2, 3, 4, 3],
    "Business_Concepts": [1, 3, 5, 2, 3, 4, 3, 5, 4, 5, 4, 5, 2, 3, 4, 5, 2, 4, 3, 5],
    "English_Proficiency": [4, 5, 3, 2, 3, 4, 5, 4, 5, 3, 2, 5, 4, 3, 5, 2, 3, 5, 4, 4],
    "Historical_Legal_Concepts": [2, 4, 5, 3, 4, 3, 5, 2, 4, 5, 3, 4, 3, 5, 4, 3, 5, 4, 2, 5],
    "Islamic_Studies": [3, 2, 5, 4, 3, 5, 2, 3, 4, 5, 2, 4, 3, 5, 2, 4, 3, 5, 3, 5],
    "Bahasa_Malaysia": [5, 3, 4, 2, 5, 4, 3, 2, 5, 3, 4, 1, 5, 3, 2, 3, 5, 4, 2, 3],
    "Problem_Solving_Enjoyment": [4, 5, 3, 2, 4, 5, 3, 2, 4, 5, 3, 2, 4, 5, 3, 2, 4, 5, 3, 2],
    "Practical_Theoretical": [3, 5, 2, 4, 5, 3, 4, 2, 5, 3, 4, 5, 3, 4, 5, 2, 4, 5, 3, 4],
    "Creativity_Level": [5, 3, 2, 4, 5, 4, 5, 3, 4, 2, 3, 5, 5, 3, 4, 5, 4, 2, 3, 5],
    "Tech_Comfort": [4, 5, 3, 2, 5, 4, 2, 3, 4, 5, 3, 2, 5, 4, 3, 5, 4, 3, 5, 2],
    "Financial_Data_Comfort": [2, 3, 5, 4, 3, 5, 4, 2, 3, 5, 4, 5, 3, 4, 5, 2, 5, 3, 4, 5],
    "Psychology_Interest": [3, 2, 4, 5, 4, 3, 5, 4, 5, 3, 2, 5, 3, 5, 4, 4, 5, 4, 3, 5],
    "Travel_Hospitality_Interest": [1, 3, 4, 5, 5, 2, 3, 5, 4, 1, 2, 4, 3, 5, 4, 2, 5, 3, 4, 3],
    "Leadership_Confidence": [3, 5, 4, 2, 5, 4, 3, 2, 5, 4, 5, 3, 4, 5, 3, 5, 4, 3, 5, 4],
    "Environment_Preference": [3, 5, 2, 4, 5, 3, 5, 4, 2, 3, 4, 3, 5, 5, 2, 4, 5, 3, 5, 2],
    "Education_Interest": [4, 2, 5, 3, 4, 5, 3, 4, 5, 2, 3, 5, 4, 3, 5, 3, 5, 4, 2, 4],
    "Course": ["Arts and Design", "Engineering", "Business", "Science", "Biotechnology", "Food Technology", "Fine Arts and Design", "Commerce", "Information Technology", "Law and Policing", "Islamic Studies and TESL", "Arts and Media", "Psychology and Health", "Education", "Travel and Hospitality", "General", "Engineering", "Science", "Biotechnology", "Food Technology"]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define features and target
X = df.drop("Course", axis=1)
y = df["Course"]

# Encode categorical data
X = pd.get_dummies(X)

# Train the decision tree model
model = DecisionTreeClassifier()
model.fit(X, y)

# Questionnaire
print("Please answer the following questions:")

def ask_question(prompt, valid_responses=None):
    while True:
        answer = input(prompt).strip()
        if valid_responses:
            if answer in valid_responses:
                return answer
            else:
                print(f"Invalid response. Please choose one of the following: {', '.join(valid_responses)}.")
        elif answer:
            return answer
        else:
            print("Input cannot be empty. Please provide a valid answer.")

# Questions 1-4 (Multiple Choice)
q1 = input("Do you consider yourself more creative, analytical, or practical? (Creative/Analytical/Practical): ")
q2 = input("Which set of skills or interests best describes you?\n" +
           "1. Problem-solving, logical thinking, and an interest in how things work.\n" +
           "2. Curiosity about nature, scientific research, and exploring how the world works.\n" +
           "3. Interest in biology, innovation, and working on solutions to health or environmental issues.\n" +
           "4. Creativity in designing or making things, especially in food or other practical applications.\n" +
           "5. Artistic talent, creativity, and a passion for visual expression.\n" +
           "6. Business-minded, with an interest in finance, marketing, or entrepreneurship.\n" +
           "7. Passion for studying law, justice, and the application of legal systems.\n" +
           "8. Interest in human behavior, mental processes, and research in psychology.\n" +
           "9. A desire to help others learn and grow through education and teaching.\n" +
           "10. Interest in managing projects, customer service, and hospitality.\n" +
           "(Enter the full description): ")
q3 = input("How do you approach solving problems: step-by-step or intuitively? (Step-by-step/Intuitively): ")
q4 = input("Are you more comfortable working with data, people, or ideas? (Data/People/Ideas): ")

# Questions 5-24 (1-5 Scale)
scores = []
questions = [
    "How confident are you in your mathematical skills?",
    "How would you rate your ability to understand and apply specific scientific concepts like biology, physics, and chemistry?",
    "How proficient are you in solving additional mathematics problems?",
    "How would you rate your artistic or visual design abilities?",
    "How comfortable are you working on experiments or lab-based tasks?",
    "How would you rate your understanding of economics, accounting, or business concepts?",
    "How confident are you in your command of the English language, both written and spoken?",
    "How skilled are you at analyzing historical or legal concepts?",
    "How strong is your grasp of Islamic Studies or moral concepts?",
    "How well do you communicate in Bahasa Malaysia?",
    "How much do you enjoy solving complex problems?",
    "How do you prefer hands-on, practical work or theoretical study?",
    "How creative are you in coming up with new ideas or designs?",
    "How comfortable are you working with technology and learning new software tools?",
    "Do you enjoy working with numbers and financial data?",
    "How much do you enjoy exploring human behavior or psychological concepts?",
    "Do you enjoy planning trips, learning about different cultures, or engaging in hospitality-related tasks?",
    "How confident are you in your ability to lead and manage projects or teams?",
    "Do you prefer working in structured environments or dynamic, creative spaces?",
    "How interested are you in contributing to society through teaching or educational programs?"
]
for i, question in enumerate(questions, start=1):
    score = int(input(f"{i}. {question} (1-5): "))
    scores.append(score)

# Prepare input data for the model
input_data = {
    "Creative_Analytical_Practical": [q1],
    "Skill_Interest_Set": [q2],
    "Problem_Solving_Approach": [q3],
    "Comfort_Working_With": [q4],
    "Mathematical_Skills": [scores[0]],
    "Scientific_Concepts": [scores[1]],
    "Additional_Maths_Skills": [scores[2]],
    "Artistic_Abilities": [scores[3]],
    "Lab_Tasks_Comfort": [scores[4]],
    "Business_Concepts": [scores[5]],
    "English_Proficiency": [scores[6]],
    "Historical_Legal_Concepts": [scores[7]],
    "Islamic_Studies": [scores[8]],
    "Bahasa_Malaysia": [scores[9]],
    "Problem_Solving_Enjoyment": [scores[10]],
    "Practical_Theoretical": [scores[11]],
    "Creativity_Level": [scores[12]],
    "Tech_Comfort": [scores[13]],
    "Financial_Data_Comfort": [scores[14]],
    "Psychology_Interest": [scores[15]],
    "Travel_Hospitality_Interest": [scores[16]],
    "Leadership_Confidence": [scores[17]],
    "Environment_Preference": [scores[18]],
    "Education_Interest": [scores[19]]
}

input_df = pd.DataFrame(input_data)
input_df = pd.get_dummies(input_df)

# Align input data with model's feature set
input_df = input_df.reindex(columns=X.columns, fill_value=0)

# Predict course
predicted_course = model.predict(input_df)[0]
print(f"Based on your responses, the recommended course is: {predicted_course}")