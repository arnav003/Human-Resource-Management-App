import re
import docx2txt
import spacy
from spacy.matcher import Matcher
import fitz


def get_category(data, category):
    try:
        return data[category]
    except:
        return None


def extract_email(text):
    email = re.findall(r"([^@|\s]+@[^@]+\.[^@|\s]+)", text)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None


def extract_mobile_number(text):
    mob_num_regex = r'''(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)
                        [-\.\s]*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'''
    phone = re.findall(re.compile(mob_num_regex), text)
    if phone:
        number = ''.join(phone[0])
        return number


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

    return parsed_data

def job_desc(desc, model="Resources/Models/output/model-best"):
    nlp = spacy.load(model)
    doc = nlp(desc)

    print(doc)

# resume_file = 'Resources/Sample Resumes/IOS1.pdf'
# text = get_text_from_pdf(resume_file)
# print(extract_data(text))

job_desc(desc='''Description
We are looking for a passionate iOS developer who can create an infrastructure for iOS app development and lead the whole process.
They will have to collaborate with cross-functional teams of talented engineers to define, design, and develop new features for next-generation applications.
Also, they will be responsible for designing and developing top-notch applications for the iOS platform, unit-testing code.
Responsibilities
Design and develop iOS compatible mobile applications
Collaborate with the design team to define the best features
Ensure quality and performance of the application
Recognize potential obstacles and fix bottlenecks
Identify and fix bugs before the final release
Publish applications on App Store
Write high-performing, scalable, reusable code
Maintain the code and atomization of the application
Design and implement updates and optimize apps
Required Skills
Bachelors degree in computer science or information technology
At least 3 years of experience in iOS app development
Strong knowledge of Objective-C, Swift, and Cocoa Touch
Vast experience with multiple iOS frameworks
Experience in continuous integration
Knowledge of iOS back-end services
Good understanding of iOS design principles and application interface guidelines
Proficiency in code versioning tools
''')
