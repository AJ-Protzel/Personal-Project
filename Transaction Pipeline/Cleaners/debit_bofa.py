# import os
# import pandas as pd

# folder_path = os.path.join('Data', 'Debit', 'BofA')

# def clean(file):
#     # file = file.iloc[6:]
#     print(f"Header of {filename}: {file.columns.tolist()}")

#     # if 'Running Bal' in file.columns:
#     #     file.drop(columns=['Running Bal'], inplace=True)

#     return file

# def transform(file):
#     return file

# for filename in os.listdir(folder_path):
#     file_path = os.path.join(folder_path, filename)
#     file = pd.read_csv(file_path, skiprows=5)

#     file = clean(file)
#     file = transform(file)

# print("Data processing complete.")


# import os
# import pandas as pd

# folder_path = os.path.join('Data', 'Debit', 'BofA')

# def print_header(file, filename):
#     print(f"Header of {filename}: {file.columns.tolist()}")

# for filename in os.listdir(folder_path):
#     file_path = os.path.join(folder_path, filename)
#     if file_path.endswith('.csv'):
#         try:
#             file = pd.read_csv(file_path, skiprows=5)
#             print_header(file, filename)
#         except pd.errors.ParserError as e:
#             print(f"Error parsing {filename}: {e}")
#         except Exception as e:
#             print(f"An unexpected error occurred with {filename}: {e}")

# print("Data processing complete.")

import os
import pandas as pd

# Define the folder path
folder_path = os.path.join('Data', 'Debit', 'BofA')

# Function to fix bad rows with improper quotations in the description column
def fix_bad_rows(df):
    df['description'] = df['description'].str.replace(r'\"', '', regex=True)
    return df

# List to store dataframes
dataframes = []

# Iterate over all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        try:
            # Read the CSV file
            df = pd.read_csv(file_path, on_bad_lines='skip')
            # Fix bad rows
            df = fix_bad_rows(df)
            # Append the dataframe to the list
            dataframes.append(df)
        except Exception as e:
            print(f"Error processing file {filename}: {e}")

# Combine all dataframes into one
if dataframes:
    combined_df = pd.concat(dataframes, ignore_index=True)
    # Print the combined dataframe
    print(combined_df)
else:
    print("No valid dataframes to concatenate.")





