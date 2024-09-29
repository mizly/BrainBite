import PyPDF2
import docx
import subprocess

def getTextFromTxt(filename):
    with open(f'{filename}', 'r', encoding='utf-8') as f:
            text = f.read()
            f.close()
    return text
def getTextFromPdf(filename):
    with open(filename, "rb") as file:
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


def getTextFromDocx(filename):
    doc = docx.Document(filename)
    text=""
    for paragraph in doc.paragraphs:
        text+=(paragraph.text + "\n")
    return text

def convert_doc_to_docx(file_path):
    output_path = file_path.replace('.doc', '.docx')
    subprocess.run(['unoconv', '-f', 'docx', file_path])
    return output_path

