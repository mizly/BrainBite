import documentReader

def process_text(filename):
    # Extract text from the uploaded file
    if filename.endswith('.txt'):  
        return  documentReader.getTextFromTxt(filename)
    if filename.endswith('.pdf'):
        return documentReader.getTextFromPdf(filename)
    if filename.endswith('.docx'):
        return documentReader.getTextFromDocx(filename)
    if filename.endswith('.doc'):
        path = documentReader.convert_doc_to_docx(filename)
        return documentReader.getTextFromDocx(path)

