# import os
# import csv
# import calendar
# import shutil

# # Define the folder paths
# folder_path = os.path.join('Data', 'Debit', 'BofA')
# clean_folder_path = os.path.join('Data', 'Clean')
# bad_lines_log_path = os.path.join(clean_folder_path, 'bad_lines.txt')
# maps_folder_path = os.path.join('Cleaners', 'Maps')
# description_map_path = os.path.join(maps_folder_path, 'Description_map.txt')
# category_map_path = os.path.join(maps_folder_path, 'Category_map.txt')

# def load_mappings(file_path):
#     mappings = {}
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as file:
#             for line in file:
#                 original, mapped = line.strip().split(',')
#                 mappings[original.lower()] = mapped
#     return mappings

# description_mappings = load_mappings(description_map_path)
# category_mappings = load_mappings(category_map_path)

# def map_description(description, amount, filename, description_mappings, category_mappings):
#     clean_description = None
#     description_lower = description.lower()
    
#     # Check if the description contains any of the keys in description_mappings
#     for original in description_mappings:
#         if original in description_lower:
#             clean_description = description_mappings[original]
#             break
    
#     if not clean_description:
#         keyword = input(f"Enter keyword to record for '{description}' in file '{filename}' with amount '{amount}': ").lower()
#         clean_description = input(f"Enter clean description for '{keyword}': ")
#         description_mappings[keyword] = clean_description
#         with open(description_map_path, 'a') as file:
#             file.write(f"{keyword},{clean_description}\n")
    
#     category = category_mappings.get(clean_description, None)
#     if not category:
#         category = input(f"Enter category for '{clean_description}': ")
#         category_mappings[clean_description] = category
#         with open(category_map_path, 'a') as file:
#             file.write(f"{clean_description},{category}\n")
    
#     return clean_description, category

# class Cleaner:
#     def __init__(self, file):
#         self.file = file
#         os.makedirs(clean_folder_path, exist_ok=True)
    
#     def remove_lines(self):
#         with open(self.file, 'r') as csvfile:
#             reader = csv.reader(csvfile)
#             # Read all lines and remove the first 6 lines
#             self.lines = list(reader)[6:]
    
#     def log_bad_lines(self):
#         cleaned_lines = []
#         with open(bad_lines_log_path, 'a') as bad_lines_log:  # Open in append mode
#             for row in self.lines:
#                 try:
#                     # Check if the row has the correct number of columns (4 in this case)
#                     if len(row) != 4:
#                         raise ValueError("Bad line")
#                     cleaned_lines.append(row)
#                 except Exception as e:
#                     # Write bad lines to the log file
#                     bad_lines_log.write(f"{self.file}: {row}\n")
#         self.cleaned_lines = cleaned_lines
    
#     def remove_empty_amount_rows(self):
#         # Remove rows where the "Amount" field (3rd column) is empty
#         self.cleaned_lines = [row for row in self.cleaned_lines if row[2].strip()]
    
#     def write_cleaned_file(self):
#         with open(self.file, 'w', newline='') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerows(self.cleaned_lines)
    
#     def clean(self):
#         self.remove_lines()
#         self.log_bad_lines()
#         self.remove_empty_amount_rows()
#         self.write_cleaned_file()

# class Transformer:
#     def __init__(self, file, description_mappings, category_mappings):
#         self.file = file
#         self.description_mappings = description_mappings
#         self.category_mappings = category_mappings
    
#     def remove_running_bal_column(self):
#         with open(self.file, 'r') as csvfile:
#             reader = csv.reader(csvfile)
#             headers = next(reader)
#             # Find the index of the "Running Bal." column
#             running_bal_index = headers.index("Running Bal.")
#             transformed_lines = [headers[:running_bal_index] + headers[running_bal_index+1:]]
#             for row in reader:
#                 transformed_row = row[:running_bal_index] + row[running_bal_index+1:]
#                 transformed_lines.append(transformed_row)
        
#         with open(self.file, 'w', newline='') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerows(transformed_lines)
    
#     def uniform_headers(self):
#         uniform_headers = ["Year", "Month", "Date", "Description", "Category", "Amount", "Account", "Bank", "Card"]
#         with open(self.file, 'r') as csvfile:
#             reader = csv.reader(csvfile)
#             next(reader)  # Skip existing headers
#             transformed_lines = [uniform_headers]
#             for row in reader:
#                 # Assuming the existing columns are in the order: Date, Description, Amount
#                 date, description, amount = row[0], row[1], row[2]
#                 year, month_num, day = date.split('/')[2], int(date.split('/')[0]), date.split('/')[1]
#                 month_str = calendar.month_name[month_num]
#                 clean_description, category = map_description(description, amount, os.path.basename(self.file), self.description_mappings, self.category_mappings)
#                 transformed_row = [year, month_str, date, clean_description, category, amount, "Debit", "BofA", "Savings"]
#                 transformed_lines.append(transformed_row)
        
#         with open(self.file, 'w', newline='') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerows(transformed_lines)

#     def transform(self):
#         self.remove_running_bal_column()
#         self.uniform_headers()

# def process_csv_files(folder_path):
#     description_mappings = load_mappings(description_map_path)
#     category_mappings = load_mappings(category_map_path)
    
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.csv'):
#             file = os.path.join(folder_path, filename)
#             cleaner = Cleaner(file)
#             cleaner.clean()  # Clean the file
#             transformer = Transformer(file, description_mappings, category_mappings)
#             transformer.transform()  # Transform the file
            
#             # Move and rename the cleaned file to Data > Clean folder
#             new_filename = f"debit_bofa_{filename}"
#             new_file_path = os.path.join(clean_folder_path, new_filename)
#             shutil.move(file, new_file_path)

#     print("Debit BofA done")  # Print completion message

# # Call the function to process CSV files
# process_csv_files(folder_path)









import os
import csv
import calendar
import shutil

# Define the folder paths
folder_path = os.path.join('Data', 'Debit', 'BofA')
clean_folder_path = os.path.join('Data', 'Clean')
bad_lines_log_path = os.path.join(clean_folder_path, 'bad_lines.txt')
maps_folder_path = os.path.join('Cleaners', 'Maps')
description_map_path = os.path.join(maps_folder_path, 'Description_map.txt')
category_map_path = os.path.join(maps_folder_path, 'Category_map.txt')

# Function to load mappings from a file
def load_mappings(file_path):
    mappings = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                original, mapped = line.strip().split(',')
                mappings[original.lower()] = mapped
    return mappings

# Function to map descriptions and categories
def map_description(description, amount, filename, description_mappings, category_mappings):
    clean_description = None
    description_lower = description.lower()
    
    # Check if the description contains any of the keys in description_mappings
    for original in description_mappings:
        if original in description_lower:
            clean_description = description_mappings[original]
            break
    
    # Prompt user for new keyword and clean description if not found
    if not clean_description:
        keyword = input(f"Enter keyword to record for '{description}' in file '{filename}' with amount '{amount}': ").lower()
        clean_description = input(f"Enter clean description for '{keyword}': ")
        description_mappings[keyword] = clean_description
        with open(description_map_path, 'a') as file:
            file.write(f"{keyword},{clean_description}\n")
    
    # Get category or prompt user for new category if not found
    category = category_mappings.get(clean_description, None)
    if not category:
        category = input(f"Enter category for '{clean_description}': ")
        category_mappings[clean_description] = category
        with open(category_map_path, 'a') as file:
            file.write(f"{clean_description},{category}\n")
    
    return clean_description, category

# Class to clean CSV files
class Cleaner:
    def __init__(self, file):
        self.file = file
        os.makedirs(clean_folder_path, exist_ok=True)
    
    def clean(self):
        # Remove the first 6 lines and log bad lines
        with open(self.file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            self.lines = list(reader)[6:]
        
        cleaned_lines = []
        with open(bad_lines_log_path, 'a') as bad_lines_log:
            for row in self.lines:
                try:
                    if len(row) != 4:
                        raise ValueError("Bad line")
                    cleaned_lines.append(row)
                except Exception as e:
                    bad_lines_log.write(f"{self.file}: {row}\n")
        
        # Remove rows with empty amount field
        self.cleaned_lines = [row for row in cleaned_lines if row[2].strip()]
        
        # Write cleaned lines back to the file
        with open(self.file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.cleaned_lines)

# Class to transform CSV files
class Transformer:
    def __init__(self, file, description_mappings, category_mappings):
        self.file = file
        self.description_mappings = description_mappings
        self.category_mappings = category_mappings
    
    def transform(self):
        # Remove "Running Bal." column and map descriptions and categories
        with open(self.file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            running_bal_index = headers.index("Running Bal.")
            transformed_lines = [headers[:running_bal_index] + headers[running_bal_index+1:]]
            for row in reader:
                transformed_row = row[:running_bal_index] + row[running_bal_index+1:]
                transformed_lines.append(transformed_row)
        
        # Uniform headers and final transformation
        uniform_headers = ["Year", "Month", "Date", "Description", "Category", "Amount", "Account", "Bank", "Card"]
        final_lines = [uniform_headers]
        for row in transformed_lines[1:]:
            date, description, amount = row[0], row[1], row[2]
            year, month_num, day = date.split('/')[2], int(date.split('/')[0]), date.split('/')[1]
            month_str = calendar.month_name[month_num]
            clean_description, category = map_description(description, amount, os.path.basename(self.file), self.description_mappings, self.category_mappings)
            final_row = [year, month_str, date, clean_description, category, amount, "Debit", "BofA", "Savings"]
            final_lines.append(final_row)
        
        # Write transformed lines back to the file
        with open(self.file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(final_lines)

# Function to process all CSV files in the specified folder
def process_csv_files(folder_path):
    description_mappings = load_mappings(description_map_path)
    category_mappings = load_mappings(category_map_path)
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file = os.path.join(folder_path, filename)
            cleaner = Cleaner(file)
            cleaner.clean()
            transformer = Transformer(file, description_mappings, category_mappings)
            transformer.transform()
            
            # Move and rename the cleaned file to Data > Clean folder
            new_filename = f"debit_bofa_{filename}"
            new_file_path = os.path.join(clean_folder_path, new_filename)
            shutil.move(file, new_file_path)

    print("Debit BofA done")

# Call the function to process CSV files
process_csv_files(folder_path)
