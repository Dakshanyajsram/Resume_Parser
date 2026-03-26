import streamlit as st
import fitz  # PyMuPDF
from docx import Document
import re
import pandas as pd
import json

st.title("Smart Resume Parser")

# -------------------------------
# 📄 Extract Text from PDF
# -------------------------------
def extract_pdf(file):
    text = ""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text

# -------------------------------
# 📄 Extract Text from DOCX
# -------------------------------
def extract_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# -------------------------------
# ✉️ Extract Email
# -------------------------------
def extract_email(text):
    match = re.findall(r'\S+@\S+', text)
    return match[0] if match else "Not found"

# -------------------------------
# 📞 Extract Phone Number
# -------------------------------
def extract_phone(text):
    match = re.findall(r'\d{10}', text)
    return match[0] if match else "Not found"

# -------------------------------
# 🧠 Extract Skills
# -------------------------------
skills_list = [
    "Python", "Java", "C", "C++", "SQL", "HTML", "CSS",
    "JavaScript", "Machine Learning", "Data Analysis"
]

def extract_skills(text):
    found_skills = []
    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)
    return found_skills

# -------------------------------
# 🎓 Extract Education
# -------------------------------
def extract_education(text):
    lines = text.split('\n')
    education_data = []
    capture = False

    for line in lines:
        line_lower = line.lower()

        # Start capturing after "education"
        if "education" in line_lower:
            capture = True
            continue

        # Stop if next section starts
        if any(word in line_lower for word in ["skills", "experience", "project", "contact"]):
            capture = False

        if capture:
            education_data.append(line.strip())

    return education_data if education_data else ["Not found"]
# -------------------------------
# 💼 Extract Experience
# -------------------------------
def extract_experience(text):
    if "experience" in text.lower():
        return "Experience section found"
    return "Not found"

# -------------------------------
# 💾 Save JSON
# -------------------------------
def save_json(data):
    with open("output.json", "w") as f:
        json.dump(data, f)

# -------------------------------
# 💾 Save CSV
# -------------------------------
def save_csv(data):
    df = pd.DataFrame([data])
    df.to_csv("output.csv", index=False)

# -------------------------------
# 📂 File Upload UI
# -------------------------------
uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

if uploaded_file:
    # Extract text
    if uploaded_file.name.endswith(".pdf"):
        text = extract_pdf(uploaded_file)
    else:
        text = extract_docx(uploaded_file)

    # Extract data
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)

    # Store in dictionary
    data = {
        "Email": email,
        "Phone": phone,
        "Skills": skills,
        "Education": education,
        "Experience": experience
    }

    # Display results
    st.write("### 📊 Extracted Information")
    st.json(data)

    # Save files
    save_json(data)
    save_csv(data)

    st.success("✅ Data saved as output.json and output.csv")
    