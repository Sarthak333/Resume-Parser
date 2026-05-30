import pdfplumber
import re
import spacy

nlp = spacy.load("en_core_web_sm")

SKILLS_LIST = [
    "python", "flask", "django", "sql", "mysql", "mongodb",
    "html", "css", "javascript", "git", "rest api", "pandas",
    "numpy", "machine learning", "data analysis", "excel"
]

def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_email(text):
    match = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match[0] if match else "Not found"

def extract_phone(text):
    match = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
    return match[0] if match else "Not found"

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Not found"

def extract_skills(text):
    text_lower = text.lower()
    found = [skill for skill in SKILLS_LIST if skill in text_lower]
    return found if found else ["No matching skills found"]

def parse_resume(pdf_path):
    print("\n========== RESUME PARSER ==========")
    text = extract_text(pdf_path)
    print(f"Name    : {extract_name(text)}")
    print(f"Email   : {extract_email(text)}")
    print(f"Phone   : {extract_phone(text)}")
    print(f"Skills  : {', '.join(extract_skills(text))}")
    print("====================================\n")

parse_resume("resume.pdf")