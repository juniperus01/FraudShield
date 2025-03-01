import fitz  # PyMuPDF for text extraction
import pdfplumber  # Extract structured tables
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    """Extracts full text from the PDF."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text

def extract_customer_info(text):
    """Extracts customer details from the bank statement."""
    doc = nlp(text)
    customer_info = {
        "customer_name": None,
        "account_no": None,
        "bank_branch": None,
        "address": None
    }

    lines = text.split("\n")
    for i, line in enumerate(lines):
        if "Name" in line or "Welcome" in line:
            customer_info["customer_name"] = lines[i + 1].strip()
        elif "Account No" in line or "SAVING ACCOUNT" in line:
            customer_info["account_no"] = lines[i + 1].strip()
        elif "Branch" in line:
            customer_info["bank_branch"] = lines[i + 1].strip()
        elif "Address" in line:
            customer_info["address"] = " ".join(lines[i + 1 : i + 4]).strip()  # Address may span multiple lines

    return customer_info

def extract_transactions_from_pdf(pdf_path):
    """Extracts structured transaction data from a PDF using pdfplumber."""
    transactions = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_table()
            if tables:
                for row in tables[1:]:  # Skip header row
                    if len(row) >= 4:  # Ensure it has enough columns
                        transactions.append({
                            "date": row[0].strip(),
                            "reference": row[1].strip(),
                            "amount": float(row[2].replace(",", "")) if row[2] else 0.0,
                            "balance": float(row[3].replace(",", "")) if row[3] else 0.0
                        })
    
    return transactions


def parse_bank_statement(pdf_path):
    """Parses both customer info and transactions from a bank statement PDF."""
    text = extract_text_from_pdf(pdf_path)
    customer_info = extract_customer_info(text)
    transactions = extract_transactions_from_pdf(pdf_path)

    return customer_info, transactions