import pdfReader
def process_text(filename):
    # Extract text from the uploaded file
    if filename.endswith('.txt'):
        with open(f'{filename}', 'r', encoding='utf-8') as f:
            text = f.read()
            f.close()
        return text
    if filename.endswith('.pdf'):
        return pdfReader.extract_text_from_pdf(filename)

