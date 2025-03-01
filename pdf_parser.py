import pdfplumber
import re
from datetime import datetime
from database import store_transaction_data


def extract_transactions_from_pdf(pdf_path):
    """Extract relevant transaction details from a bank statement PDF."""
    transactions = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split("\n")

                for line in lines:
                    # Regex pattern to match transaction details (Date, Amount, Sender, Receiver, Type)
                    match = re.search(r"(\d{2}/\d{2}/\d{4})\s+([\d,]+\.\d{2})\s+(\w+)\s+(\w+)\s+(\w+)", line)
                    if match:
                        date_str, amount, sender, receiver, transaction_type = match.groups()

                        # Convert date format
                        transaction_date = datetime.strptime(date_str, "%d/%m/%Y").date()

                        transactions.append({
                            "customer_name": "Unknown",  # Will be updated later
                            "account_no": "Unknown",
                            "bank_branch": "Unknown",
                            "credit_score": 0,  # Placeholder, update if available
                            "date": transaction_date,
                            "amount": float(amount.replace(",", "")),  # Remove commas and convert to float
                            "sender_id": sender,
                            "receiver_id": receiver,
                            "transaction_type": transaction_type
                        })

    return transactions


# Test with a sample PDF
if __name__ == "__main__":
    pdf_path = "sample_bank_statement.pdf"  # Replace with your PDF file path
    extracted_data = extract_transactions_from_pdf(pdf_path)
    store_transaction_data(extracted_data)
    print("Transactions extracted and stored successfully!")
