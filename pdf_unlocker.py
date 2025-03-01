from pypdf import PdfReader, PdfWriter

input_pdf = "sbi_bank_statement.pdf"
output_pdf = "sample_sbi_bank_statement.pdf"
password = "93220040903"

reader = PdfReader(input_pdf)
if reader.decrypt(password):  # Try to decrypt
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)
    print("PDF unlocked successfully!")
else:
    print("Incorrect password or unable to unlock.")
