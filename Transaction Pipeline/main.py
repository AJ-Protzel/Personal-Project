import os
import csv
import calendar
import shutil
import json
import sys

# Static paths
CLEAN_FOLDER_PATH = os.path.join('Data', 'Clean')
BAD_LINES_LOG_PATH = os.path.join(CLEAN_FOLDER_PATH, 'bad_lines.txt')
MAPS_FOLDER_PATH = os.path.join('Configs', 'Maps')
DESCRIPTION_MAP_PATH = os.path.join(MAPS_FOLDER_PATH, 'Description_map.txt')
CATEGORY_MAP_PATH = os.path.join(MAPS_FOLDER_PATH, 'Category_map.txt')
UNIFORM_HEADERS = ["Year", "Month", "Date", "Description", "Category", "Amount", "Account", "Bank", "Card"]

def load_config(config_path):
    """Load configuration from a JSON file."""
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config

def load_mappings(file_path):
    """Load mappings from a file."""
    mappings = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                original, mapped = line.strip().split(',')
                mappings[original.lower()] = mapped
    return mappings

def clean_csv(file, config):
    """Clean the CSV file by removing extra headers and logging bad lines."""
    print(f"Cleaning file: {file}")
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        lines = list(reader)[config['REMOVE_ROW']:]
        
        cleaned_lines = []
        with open(BAD_LINES_LOG_PATH, 'a') as bad_lines_log:
            for row in lines:
                try:
                    if len(row) != len(lines[0]):
                        raise ValueError("Bad line")
                    cleaned_lines.append(row)
                except Exception as e:
                    bad_lines_log.write(f"{file}: {row}\n")
        
        amount_index = config['HEADER_MAPPING'].get("Amount", None)
        if amount_index is not None:
            amount_index = lines[0].index(amount_index)
            cleaned_lines = [row for row in cleaned_lines if row[amount_index].strip()]
        else:
            print("Warning: 'Amount' column not found in HEADER_MAPPING.")
        
        with open(file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(cleaned_lines)

def map_description(description, amount, filename, description_mappings, category_mappings):
    """Map descriptions and categories based on mappings or prompt user for new mappings."""
    clean_description = None
    description_lower = description.lower()
    
    for original in description_mappings:
        if original in description_lower:
            clean_description = description_mappings[original]
            break
    
    if not clean_description:
        keyword = input(f"Enter keyword to record for '{description}' in file '{filename}' with amount '{amount}': ").lower()
        clean_description = input(f"Enter clean description for '{keyword}': ")
        description_mappings[keyword] = clean_description
        with open(DESCRIPTION_MAP_PATH, 'a') as file:
            file.write(f"{keyword},{clean_description}\n")
    
    category = category_mappings.get(clean_description, None)
    if not category:
        categories = [
            "Bills & Utilities",
            "Cash",
            "Gas",
            "Groceries",
            "Restaurant",
            "Shopping"
        ]
        
        print(f"Possible categories for '{clean_description}':")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        
        category_choice = input("Enter the number corresponding to the category or type a new category: ")
        
        if category_choice.isdigit() and 1 <= int(category_choice) <= len(categories):
            category = categories[int(category_choice) - 1]
        else:
            category = category_choice
        
        category_mappings[clean_description] = category
        with open(CATEGORY_MAP_PATH, 'a') as file:
            file.write(f"{clean_description},{category}\n")
    
    return clean_description, category

def transform_csv(file, config, description_mappings, category_mappings):
    """Transform the CSV file by removing specified columns and mapping headers."""
    print(f"Transforming file: {file}")
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        indices_to_delete = [headers.index(col) for col in config['REMOVE_COL'] if col in headers]
        transformed_lines = [[col for i, col in enumerate(headers) if i not in indices_to_delete]]
        for row in reader:
            transformed_row = [col for i, col in enumerate(row) if i not in indices_to_delete]
            transformed_lines.append(transformed_row)
        
        final_lines = [UNIFORM_HEADERS]
        for row in transformed_lines[1:]:
            mapped_row = {config['HEADER_MAPPING'].get(header, header): value for header, value in zip(transformed_lines[0], row)}
            
            date_str = mapped_row.get("Date", "")
            if date_str:
                year, month_num, day = date_str.split('/')[2], int(date_str.split('/')[0]), date_str.split('/')[1]
                month_str = calendar.month_name[month_num]
            else:
                year, month_str = "", ""
            
            # Convert amount to a number
            amount_str = mapped_row.get("Amount", "").replace(",", "")
            amount_num = float(amount_str) if amount_str else ""
            
            final_row = [
                year,
                month_str,
                date_str,
                mapped_row.get("Description", ""),
                "", # Placeholder for category to be filled later
                amount_num,
                config['ACCOUNT'],
                config['BANK'],
                config['CARD']
            ]
            
            final_lines.append(final_row)
        
        # Remove rows where the 'Amount' field is empty
        amount_index_final = UNIFORM_HEADERS.index("Amount")
        final_lines = [row for row in final_lines if row[amount_index_final] != ""]
        
        # Map descriptions and categories after removing empty amount rows
        for i in range(1, len(final_lines)):
            final_lines[i][3], final_lines[i][4] = map_description(final_lines[i][3], final_lines[i][5], os.path.basename(file), description_mappings, category_mappings)
        
        with open(file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(final_lines)

def process_csv_files(config_path):
    """Process all CSV files in the specified folder."""
    config = load_config(config_path)
    
    description_mappings = load_mappings(DESCRIPTION_MAP_PATH)
    category_mappings = load_mappings(CATEGORY_MAP_PATH)
    
    print(f"Processing files in folder: {config['FOLDER_PATH']}")
    
    for filename in os.listdir(config['FOLDER_PATH']):
        if filename.lower().endswith('.csv'):
            file = os.path.join(config['FOLDER_PATH'], filename)
            print(f"Found CSV file: {file}")
            clean_csv(file, config)
            transform_csv(file, config, description_mappings, category_mappings)
            
            new_filename = f"{config['ACCOUNT']}_{config['BANK']}_{config['CARD']}_{filename}"
            new_file_path = os.path.join(CLEAN_FOLDER_PATH, new_filename)
            shutil.move(file, new_file_path)
            print(f"Processed and moved file to: {new_file_path}")
        else:
            print(f"Skipping non-CSV file: {filename}")

def run_cleaner(config_path):
    """Run the cleaner program with the specified configuration file."""
    process_csv_files(config_path)

if __name__ == "__main__":
    configs_folder = 'Configs'
    
    if not os.path.exists(configs_folder):
        sys.exit(1)
    configs = [os.path.join(configs_folder, config) for config in os.listdir(configs_folder) if config.endswith('.json')]
    
    if not configs:
        sys.exit(1)
    for config in configs:
        run_cleaner(config)
