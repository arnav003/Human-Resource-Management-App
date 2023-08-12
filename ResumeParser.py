import re
import docx2txt
import spacy
from spacy.matcher import Matcher
import fitz


def get_category(data, category):
    try:
        value = data[category]
        if not isinstance(value, list):
            value = [value, ]
        return value
    except:
        return None


def extract_email(text):
    email = re.findall(r"([^@|\s]+@[^@]+\.[^@|\s]+)", text)
    if email:
        try:
            return [email[0].split()[0].strip(';'), ]
        except IndexError:
            return None


def extract_mobile_number(text):
    mob_num_regex = r'''(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)
                        [-\.\s]*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'''
    phone = re.findall(re.compile(mob_num_regex), text)
    if phone:
        number = ''.join(phone[0])
        return [number, ]


def get_text_from_docx(doc_path):
    try:
        temp = docx2txt.process(doc_path)
        text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
        return ' '.join(text)
    except KeyError:
        return ' '


def get_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = " "
    for page in doc:
        text = text + str(page.get_text())

    return text


def extract_data(text, model="Resources/Models/output/model-best"):
    nlp = spacy.load(model)
    doc = nlp(text)

    resume_data = {}
    for ent in doc.ents:
        if ent.label_ in resume_data.keys():
            resume_data[ent.label_].append(ent.text)
        else:
            resume_data[ent.label_] = [ent.text, ]
    print(resume_data)
    parsed_data = {}

    parsed_data["name"] = get_category(resume_data, "NAME")
    parsed_data["phone number"] = extract_mobile_number(text)
    parsed_data["email"] = extract_email(text)
    parsed_data["linkedin"] = get_category(resume_data, "LINKEDIN LINK")
    parsed_data["degree"] = get_category(resume_data, "DEGREE")
    parsed_data["year of graduation"] = get_category(resume_data, "YEAR OF GRADUATION")
    parsed_data["university"] = get_category(resume_data, "UNIVERSITY")
    parsed_data["skills"] = get_category(resume_data, "SKILLS")
    parsed_data["certification"] = get_category(resume_data, "CERTIFICATION")
    parsed_data["awards"] = get_category(resume_data, "AWARDS")
    parsed_data["worked as"] = get_category(resume_data, "WORKED AS")
    parsed_data["companies worked at"] = get_category(resume_data, "COMPANIES WORKED AT")
    parsed_data["years of experience"] = get_category(resume_data, "YEARS OF EXPERIENCE")
    parsed_data["language"] = get_category(resume_data, "LANGUAGE")

    print(parsed_data)

    return parsed_data


def parse_job_desc(desc, model="Resources/Models/output/model-best"):
    nlp = spacy.load(model)
    doc = nlp(desc)

    for ent in doc.ents:
        print(ent.text + " -> " + ent.label_)


# resume_file = 'Resources/Sample Resumes/IOS1.pdf'
# text = get_text_from_pdf(resume_file)
# print(extract_data(text))

# test_str = "My name is Arnav. I am studying B.Tech Computer Science Engineering at Manipal University Jaipur."
# parse_job_desc(desc=test_str, model="en_core_web_sm")

file = open('job_desc.txt', 'r')
desc = file.read()
file.close()

parse_job_desc(desc=desc)

# file = open("resume_text.txt", 'w')
# file.write(text)
# file.close()
