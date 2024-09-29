import PyPDF2

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        full_text = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)
        combined_text = "\n".join(full_text)
        lines = combined_text.splitlines()
        text = ""
        for line in [line.strip() for line in lines if line.strip()]:
            text+=(line+" ")

        return text


