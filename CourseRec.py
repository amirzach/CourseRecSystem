import pandas as pd

# Function to infer courses based on the rule set
def infer_course(row):
    # Extract grades for relevant subjects
    math = row['MATEMATIK']
    add_math = row['MATEMATIK TAMBAHAN']
    physics = row['FIZIK']
    biology = row['BIOLOGI']
    chemistry = row['KIMIA']
    bm = row['BAHASA MALAYSIA']
    bi = row['BAHASA INGGERIS']
    seni = row['PENDIDIKAN SENI VISUAL']
    economics = row['EKONOMI']
    perniagaan = row['PERNIAGAAN']
    perakaunan = row['PRINSIP PERAKAUNAN']

    # Rules for course inference
    if math in ['A', 'A-'] and add_math in ['A', 'A-'] and physics in ['A', 'B', 'A-']:
        return 'Engineering'
    elif biology in ['A', 'A-'] and physics in ['A', 'B', 'A-'] and chemistry in ['A', 'A-', 'B']:
        return 'Science'
    elif bm in ['A', 'A-', 'B'] and bi in ['A', 'A-', 'B'] and seni in ['A', 'B']:
        return 'Arts'
    elif economics in ['A', 'B'] or perniagaan in ['A', 'B'] or perakaunan in ['A', 'B']:
        return 'Commerce'
    else:
        return 'General'

# Load the Excel file
file_path = r'C:\Users\User\spmresultsdataset_fyphelper.xlsx'
data = pd.read_excel(file_path)

# Clean column names
data.columns = data.columns.str.strip().str.replace('\n', '').str.upper()

# Drop irrelevant columns
columns_to_drop = ['NAMA', 'ANGKA GILIRAN']
data_cleaned = data.drop(columns=columns_to_drop, errors='ignore')

# Apply the rule-based inference
data_cleaned['Recommended Course'] = data_cleaned.apply(infer_course, axis=1)

# Save the result to a new Excel file
output_path = r'C:\Users\User\recommended_courses.xlsx'
data_cleaned.to_excel(output_path, index=False)

print(f"Course recommendations saved to {output_path}")
