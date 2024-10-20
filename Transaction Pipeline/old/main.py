import pandas as pd
import os

# Define a mapping of your CSV headers to a common format
header_mapping = {
    'CreditAmazon': {'Transaction Date': 'Transaction Date', 'Amount': 'Transaction Amount', 'Description': 'Transaction Description'},
    'CreditSapphire': {'Transaction Date': 'Transaction Date', 'Amount': 'Transaction Amount', 'Description': 'Transaction Description'},
    'SavingsBofA': {'Date': 'Transaction Date', 'Amount': 'Transaction Amount', 'Description': 'Transaction Description'},
    'CreditBofA': {'Posted Date': 'Transaction Date', 'Amount': 'Transaction Amount', 'Payee': 'Transaction Description'},
    'CreditBilt': {'Date': 'Transaction Date', 'Amount': 'Transaction Amount', 'Description': 'Transaction Description'},
    'Wellsfargo': {'Date': 'Transaction Date', 'Amount': 'Transaction Amount', 'Description': 'Transaction Description'},
    'BofA': {'Posted Date': 'Transaction Date', 'Amount': 'Transaction Amount', 'Reference Number': 'Transaction Description'},  # Ensure this line is correct
    # Add more mappings for other banks as needed
}

# Function to standardize the headers and add additional columns
def standardize_headers(df, bank_name, account_type, card):
    if bank_name in header_mapping:
        df = df.rename(columns=header_mapping[bank_name])
    else:
        raise KeyError(f"Header mapping for bank '{bank_name}' not found.")
    df['Account type'] = account_type
    df['Bank'] = bank_name
    df['Card'] = card
    df['Month'] = pd.to_datetime(df['Transaction Date']).dt.strftime('%B')
    df['Year'] = pd.to_datetime(df['Transaction Date']).dt.year
    return df[['Month', 'Year', 'Transaction Date', 'Transaction Description', 'Transaction Amount', 'Account type', 'Bank', 'Card']]

# Function to adjust amounts based on account type
def adjust_amounts(df, account_type):
    if account_type == 'credit':
        df['Transaction Amount'] = df['Transaction Amount'].apply(lambda x: -x if x > 0 else x)
    return df

# Initialize an empty DataFrame to hold all transactions
all_transactions = pd.DataFrame()

# Traverse the directory tree
for root, dirs, files in os.walk('Data'):
    print(f"Traversing directory: {root}")  # Debugging print statement
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(root, file)
            print(f"Processing file: {file_path}")  # Debugging print statement
            # Determine the bank name, account type, and card based on the folder structure
            parts = root.split(os.sep)
            if len(parts) >= 3 and parts[-3].lower() == "data":
                if parts[-2].lower() == "savings":
                    account_type = "savings"
                    card = "Savings"
                    if parts[-1].lower() == "bofa":
                        bank_name = "BofA"
                    else:
                        print(f"Skipping unknown savings account: {root}")  # Debugging print statement
                        continue  # Skip unknown savings accounts
                elif parts[-2].lower() == "credit":
                    account_type = "credit"
                    if parts[-1].lower() == "amazon":
                        bank_name = "Chase"
                        card = "Amazon"
                    elif parts[-1].lower() == "sapphire":
                        bank_name = "Chase"
                        card = "Sapphire"
                    elif parts[-1].lower() == "bofa":
                        bank_name = "BofA"
                        card = "CashBack"
                    elif parts[-1].lower() == "bilt":
                        bank_name = "Wellsfargo"
                        card = "Bilt"
                    else:
                        print(f"Skipping unknown credit card: {root}")  # Debugging print statement
                        continue  # Skip unknown credit cards
                else:
                    print(f"Skipping unknown account type: {root}")  # Debugging print statement
                    continue  # Skip unknown account types
            else:
                print(f"Skipping unknown folder structure: {root}")  # Debugging print statement
                continue  # Skip unknown folder structures

            # Read the CSV file into a DataFrame, handling cases with no headers
            try:
                if bank_name == "BofA" and account_type == "savings":
                    df = pd.read_csv(file_path, skiprows=5)  # Adjust the number of rows to skip based on your file
                elif bank_name == "Wellsfargo" and card == "Bilt":
                    df = pd.read_csv(file_path, header=None, names=["Date", "Amount", "Unused1", "Unused2", "Description"])
                else:
                    df = pd.read_csv(file_path)
                print(f"Data from {file_path}:\n{df.head()}")  # Debugging print statement
            except Exception as e:
                print(f"Error reading {file_path}: {e}")  # Debugging print statement
                continue

            # Standardize the headers and add additional columns
            df = standardize_headers(df, bank_name, account_type, card)
            # Adjust amounts based on account type
            df = adjust_amounts(df, account_type)
            # Append the DataFrame to the consolidated DataFrame
            all_transactions = pd.concat([all_transactions, df], ignore_index=True)

# Save the consolidated DataFrame to a new CSV file with the specified header
all_transactions.to_csv('main.csv', index=False)

# Print the consolidated DataFrame for debugging purposes
print(all_transactions)
