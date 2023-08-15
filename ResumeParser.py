import re
import docx2txt
import spacy
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

    # file = open('resume_text.txt', 'w')
    # file.write(text)
    # file.close()

    return text


def extract_data(text, model="Resources/Models/output/model-best"):
    nlp = spacy.load(model)
    doc = nlp(text)

    resume_data = {}
    data_str = ''
    for ent in doc.ents:
        if ent.label_ in resume_data.keys():
            resume_data[ent.label_].append(ent.text)
        else:
            resume_data[ent.label_] = [ent.text, ]
        data_str += ent.text + " -> " + ent.label_ + '\n'

    data_dict = {}

    data_dict["name"] = get_category(resume_data, "NAME")
    data_dict["phone number"] = extract_mobile_number(text)
    data_dict["email"] = extract_email(text)
    data_dict["linkedin"] = get_category(resume_data, "LINKEDIN LINK")
    data_dict["degree"] = get_category(resume_data, "DEGREE")
    data_dict["year of graduation"] = get_category(resume_data, "YEAR OF GRADUATION")
    data_dict["university"] = get_category(resume_data, "UNIVERSITY")
    data_dict["skills"] = get_category(resume_data, "SKILLS")
    data_dict["certification"] = get_category(resume_data, "CERTIFICATION")
    data_dict["awards"] = get_category(resume_data, "AWARDS")
    data_dict["worked as"] = get_category(resume_data, "WORKED AS")
    data_dict["companies worked at"] = get_category(resume_data, "COMPANIES WORKED AT")
    data_dict["years of experience"] = get_category(resume_data, "YEARS OF EXPERIENCE")
    data_dict["language"] = get_category(resume_data, "LANGUAGE")

    # print(data_dict)
    # file = open('resume_data.txt', 'w')
    # file.write(data_str)
    # file.close()

    return data_dict, data_str


def parse_job_desc(desc, model="Resources/Models/output/model-best"):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(desc)

    # nlp = spacy.load(model)
    # doc = nlp(desc)

    for ent in doc.ents:
        print(ent.text + " -> " + ent.label_)


# resume_file = 'Resources/Sample Resumes/IOS1.pdf'
# text = get_text_from_pdf(resume_file)
# data_dict, data_str = extract_data(text)

# file = open('job_desc.txt', 'r')
# desc = file.read()
# parse_job_desc(desc=desc)
# file.close()
#
# data_lg = extract_data(text, model='en_core_web_lg')
# file_lg = open("resume_data_lg.txt", 'w')
# file_lg.write(data_lg)
# file_lg.write("\n\nrunning on resume parser model\n\n")
# data_lg = extract_data(data_lg)
# file_lg.write(data_lg)
# file_lg.close()
#
# data_md = extract_data(text, model='en_core_web_md')
# file_md = open("resume_data_md.txt", 'w')
# file_md.write(data_md)
# file_md.write("\n\nrunning on resume parser model\n\n")
# data_md = extract_data(data_md)
# file_md.write(data_md)
# file_md.close()
#
# data_sm = extract_data(text, model='en_core_web_sm')
# file_sm = open("resume_data_sm.txt", 'w')
# file_sm.write(data_sm)
# file_sm.write("\n\nrunning on resume parser model\n\n")
# data_sm = extract_data(data_sm)
# file_sm.write(data_sm)
# file_sm.close()