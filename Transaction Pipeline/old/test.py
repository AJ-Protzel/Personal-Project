import pandas as pd
import os

class TransactionProcessor:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.header_mapping = {
            'CreditAmazon': {'Transaction Date': 'Transaction Date', 'Amount': 'Transaction Amount', 'Description': 'Transaction Description'},
            'CreditSapphire': {'Transaction Date': 'Transaction Date', 'Amount': 'Transaction Amount', 'Description': 'Transaction Description'},
            'SavingsBofA': {'Date': 'Transaction Date', 'Amount': 'Transaction Amount', 'Description': 'Transaction Description'},
            'CreditBofA': {'Posted Date': 'Transaction Date', 'Amount': 'Transaction Amount', 'Payee': 'Transaction Description'},
            'CreditBilt': {'Date': 'Transaction Date', 'Amount': 'Transaction Amount', 'Description': 'Transaction Description'},
        }
        self.all_transactions = pd.DataFrame()

    def standardize_headers(self, df, bank_name, account_type, card):
        df = df.rename(columns=self.header_mapping[bank_name])
        df['Account type'] = account_type
        df['Bank'] = bank_name
        df['Card'] = card
        df['Month'] = pd.to_datetime(df['Transaction Date']).dt.strftime('%B')
        df['Year'] = pd.to_datetime(df['Transaction Date']).dt.year
        return df[['Month', 'Year', 'Transaction Date', 'Transaction Description', 'Transaction Amount', 'Account type', 'Bank', 'Card']]

    def adjust_amounts(self, df, account_type):
        if account_type == 'credit':
            df['Transaction Amount'] = df['Transaction Amount'].apply(lambda x: -x if x > 0 else x)
        return df

    def process_file(self, file_path, bank_name, account_type, card):
        try:
            if bank_name == "BofA" and account_type == "savings":
                df = pd.read_csv(file_path, skiprows=5)
            elif bank_name == "Wellsfargo" and card == "Bilt":
                df = pd.read_csv(file_path, header=None, names=["Date", "Amount", "Unused1", "Unused2", "Description"])
            else:
                df = pd.read_csv(file_path)
            
            df = self.standardize_headers(df, bank_name, account_type, card)
            df = self.adjust_amounts(df, account_type)
            self.all_transactions = pd.concat([self.all_transactions, df], ignore_index=True)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    def traverse_and_process(self):
        for root, dirs, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    parts = root.split(os.sep)
                    if len(parts) >= 3 and parts[-3].lower() == "data":
                        if parts[-2].lower() == "savings":
                            account_type = "savings"
                            card = "Savings"
                            if parts[-1].lower() == "bofa":
                                bank_name = "BofA"
                            else:
                                continue
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
                                continue
                        else:
                            continue
                        self.process_file(file_path, bank_name, account_type, card)

    def save_to_csv(self, output_file):
        self.all_transactions.to_csv(output_file, index=False)

if __name__ == "__main__":
    processor = TransactionProcessor(data_dir='Data')
    processor.traverse_and_process()
    processor.save_to_csv('main.csv')
