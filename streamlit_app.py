import streamlit as st
import database as db
import base64
import time
import datetime
import ResumeParser
from PIL import Image


@st.cache_resource
def get_resume_text(path):
    text = ResumeParser.get_text_from_pdf(path)
    return text


@st.cache_resource
def get_data(text):
    data_str, data_json = ResumeParser.extract_data_chatgpt(text)
    return data_str, data_json


@st.cache_resource
def get_questions(data):
    data_str, data_json = ResumeParser.generate_questions_chatgpt(data)
    try:
        questions = data_json['questions']
    except TypeError:
        questions = None
    return data_str, questions


@st.cache_resource
def get_analyis(text, job_desc):
    data_str, data_json = ResumeParser.analyze_resume_chatgpt(text, job_desc)
    return data_str, data_json


def get_detail(value, text, is_display=True):
    out = ""
    if is_display:
        col1, col2 = st.columns([1, 5])
        col1.write(f'{text}: ')
    if isinstance(value, list):
        if value != [] and value[0] != "Not found":
            for ele in value:
                out = out + ele + "\n"
                if is_display:
                    col2.text(ele)
        else:
            out = "Not found."
            if is_display:
                col2.error(f"{text} not found.")
    else:
        out = value
        if is_display:
            if value != 'Not found':
                col2.text(value)
            else:
                col2.error(f"{text} not found.")

    return out


def get_table_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href


def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.subheader("**Uploaded Resume**")
    with st.expander("Show Resume"):
        st.markdown(pdf_display, unsafe_allow_html=True)


def run():
    col1, col2 = st.sidebar.columns([1, 3])
    img = Image.open('./Resources/Images/Logo_3.png')
    img = img.resize((100, 75))
    col1.image(img)
    col2.markdown("# Recruit Ranker")

    st.sidebar.markdown("# Choose User")
    activities = ["User", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)

    user_data_table = st.secrets.connections.mysql.user_data

    if choice == 'User':
        pdf_file = st.sidebar.file_uploader('Choose your Resume', type=["pdf"])
        if pdf_file is not None:
            pdf_file_path = "./Uploaded Resumes/" + pdf_file.name
            with open(pdf_file_path, "wb") as f:
                f.write(pdf_file.getbuffer())

            text = get_resume_text(pdf_file_path)
            _, resume_data = get_data(text)

            if resume_data:
                st.header("Hello, " + get_detail(resume_data['name'], "Name", False))

                st.markdown('''---''')

                show_pdf(pdf_file_path)

                st.subheader("**Resume Details**")

                with st.expander("Show Details"):
                    name = get_detail(resume_data['name'], "Name")
                    email = get_detail(resume_data['email'], "Email")
                    phone = get_detail(resume_data['phone_number'], "Phone Number")
                    linkedin = get_detail(resume_data['linkedin'], "LinkedIn")
                    date_of_birth = get_detail(resume_data["date_of_birth"], "Date of Birth")
                    address = get_detail(resume_data["address"], "Address")
                    skills = get_detail(resume_data["skills"], "Skills")
                    projects = get_detail(resume_data["project_descriptions"], "Projects")
                    degree = get_detail(resume_data["degrees"], "Degree")
                    year_of_graduation = get_detail(resume_data["year_of_graduation"], "Year of Graduation")
                    university = get_detail(resume_data["college_name"], "College")
                    certification = get_detail(resume_data["certifications"], "Certification")
                    awards = get_detail(resume_data["awards"], "Awards")
                    worked_as = get_detail(resume_data["worked_as"], "Worked As")
                    companies_worked_at = get_detail(resume_data["companies_worked_at"],
                                                     "Companies Worked At")
                    research_paper = get_detail(resume_data["research_papers"], "Research Papers")
                    years_of_experience = get_detail(resume_data["years_of_experience"],
                                                     "Years of Experience")
                    language = get_detail(resume_data["natural_languages"], "Language")

                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date + '_' + cur_time)

                st.subheader("**Resume Analysis**")

                with st.expander(label='Show Analysis'):
                    job_desc_file_path = "./Resources/Sample Job Descriptions/job_desc_1.txt"
                    with open(job_desc_file_path, "r") as f:
                        job_desc = f.read()

                    _, analysis = get_analyis(text, job_desc)

                    resume_score = 0
                    for i, score in enumerate(analysis['scores']):
                        resume_score = resume_score + score
                        st.markdown(f'''{i + 1}. {analysis['reasons'][i]}''')
                        if score > 6:
                            st.success(f'''Score: {score}''')
                        else:
                            st.warning(f'''Score: {score}''')

                    st.subheader("**Resume Score**")
                    st.markdown(
                        """
                        <style>
                            .stProgress > div > div > div > div {
                                background-color: #d73b5c;
                            }
                        </style>""",
                        unsafe_allow_html=True,
                    )
                    my_bar = st.progress(0)
                    score = 0
                    max_score = 60
                    score_percent = (int)((resume_score / max_score) * 100)
                    for percent_complete in range(score_percent):
                        score += 1
                        time.sleep(0.01)
                        my_bar.progress(percent_complete + 1)
                    st.success(f'**Your Resume Score: {str(resume_score)} / {str(max_score)}**')

                st.subheader("**Interview Questions**")
                with st.expander(label="Show Questions"):
                    _, questions = get_questions(resume_data)
                    answers = []
                    for question in questions:
                        answer = st.text_input(label=f'{question}?')
                        answers.append(answer)

                db.insert_user_data(user_data_table, timestamp, name, email, linkedin, phone, skills, str(resume_score))
            else:
                st.error('Something went wrong..')
    else:
        if st.session_state['admin_logged_in'] == False:
            st.markdown('### Welcome to Admin Portal')
            ad_user = st.text_input("Username")
            ad_password = st.text_input("Password", type='password')
            if st.button('Login'):
                if ad_user == 'admin' and ad_password == '123456':
                    st.session_state['admin_logged_in'] = True
                else:
                    st.error("Wrong ID or Password.")
        else:
            st.success("Welcome Admin")

            st.markdown('### Admin Portal')

            with st.expander(label="User Data", expanded=False):
                user_data_df = db.get_user_data(user_data_table)
                st.dataframe(user_data_df)

                st.markdown(get_table_download_link(user_data_df, "user_data.csv", "Download User Data"),
                            unsafe_allow_html=True)

            listing_data_table = st.secrets.connections.mysql.listing_table

            with st.expander(label="Listing Data", expanded=False):
                listing_data_df = db.get_listing_data(listing_data_table)
                st.dataframe(listing_data_df)

                st.markdown(get_table_download_link(listing_data_df, "listing_data.csv", "Download Listing Data"),
                            unsafe_allow_html=True)

            with st.expander(label="Add new listing", expanded=False):
                job_desc = st.text_input("Job Description")
                job_res = st.text_input("Job Responsibilities")
                job_skills = st.text_input("Job Skills")

                if st.button('Add listing'):
                    db.insert_listing_data(listing_data_table, job_desc, job_res, job_skills)


if 'admin_logged_in' not in st.session_state:
    st.session_state['admin_logged_in'] = False
if 'connection_object' not in st.session_state:
    st.session_state['connection_object'] = None

st.set_page_config(
    page_title="Recruit Ranker",
    page_icon='./Resources/Images/Logo_4.png',
    layout='centered',
)

if st.session_state['connection_object'] is None:
    connection = db.set_connection()

if not db.check_connection():
    connection = db.set_connection()
cursor = db.set_cursor()

# db.init()

run()
