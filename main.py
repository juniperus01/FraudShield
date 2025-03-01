from pdf_extractor import extract_text_from_pdf, extract_tables_from_pdf, parse_bank_statement
from ocr_processor import extract_text_from_scanned_pdf
from nlp_processor import extract_entities
from database import store_transaction_data

PDF_PATH = "sample_sbi_bank_statement.pdf"


def main():
    customer_info, transactions_data = parse_bank_statement(PDF_PATH)

    # Store extracted transactions in the database
    store_transaction_data(formatted_transactions)
    print("✅ Data successfully stored in SQLite!")


if __name__ == "__main__":
    main()
