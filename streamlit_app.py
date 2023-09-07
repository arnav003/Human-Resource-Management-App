import streamlit as st
import database as db
import base64
import time
import datetime
import ResumeParser
from PIL import Image


@st.cache_resource
def get_data(save_image_path):
    text = ResumeParser.get_text_from_pdf(save_image_path)
    # data, _ = ResumeParser.extract_data_llama(text)
    # data = ResumeParser.test_extract_data()
    data = ResumeParser.extract_data_chatgpt(text)
    return data


def print_list_with_text(value, text, print_list=True):
    out = ""
    if print_list:
        col1, col2 = st.columns([1, 5])
        col1.write(f'{text}: ')
    if isinstance(value, list):
        if value != [] and value[0] != "Not found":
            for ele in value:
                out = out + ele + "\n"
                if print_list:
                    col2.text(ele)
        else:
            out = "Not found."
            if print_list:
                col2.error(f"{text} not found.")
    else:
        out = value
        if print_list:
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
    with st.expander("Show CV"):
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
        pdf_file = st.file_uploader('Choose your Resume', type=["pdf"])
        if pdf_file is not None:
            save_image_path = "./Uploaded Resumes/" + pdf_file.name
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            resume_data = get_data(save_image_path)

            if resume_data:
                st.header("Hello, " + print_list_with_text(resume_data['name'], "Name", print_list=False))

                show_pdf(save_image_path)

                with st.expander("Extracted Details"):
                    name = print_list_with_text(resume_data['name'], "Name")
                    email = print_list_with_text(resume_data['email'], "Email")
                    phone = print_list_with_text(resume_data['phone_number'], "Phone Number")
                    linkedin = print_list_with_text(resume_data['linkedin'], "LinkedIn")
                    date_of_birth = print_list_with_text(resume_data["date_of_birth"], "Date of Birth")
                    address = print_list_with_text(resume_data["address"], "Address")
                    skills = print_list_with_text(resume_data["skills"], "Skills")
                    projects = print_list_with_text(resume_data["project_descriptions"], "Projects")
                    degree = print_list_with_text(resume_data["degrees"], "Degree")
                    year_of_graduation = print_list_with_text(resume_data["year_of_graduation"], "Year of Graduation")
                    university = print_list_with_text(resume_data["college_name"], "College")
                    certification = print_list_with_text(resume_data["certifications"], "Certification")
                    awards = print_list_with_text(resume_data["awards"], "Awards")
                    worked_as = print_list_with_text(resume_data["worked_as"], "Worked As")
                    companies_worked_at = print_list_with_text(resume_data["companies_worked_at"],
                                                               "Companies Worked At")
                    research_paper = print_list_with_text(resume_data["research_papers"], "Research Papers")
                    years_of_experience = print_list_with_text(resume_data["years_of_experience"],
                                                               "Years of Experience")
                    language = print_list_with_text(resume_data["natural_languages"], "Language")

                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date + '_' + cur_time)

                st.subheader("**Resume Analysis**")
                resume_score = 0

                if resume_data['degrees'] is not None or resume_data['college_name'] is not None:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>
                        [+] Awesome! You have added your Degree.</h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #fabc10;'>
                        [-] Please add your Degree.</h4>''',
                        unsafe_allow_html=True)

                if resume_data['worked_as'] is not None:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>
                        [+] Awesome! You have added your Previous Experiences.</h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #fabc10;'>
                        [-] Please add your Previous Experiences.</h4>''',
                        unsafe_allow_html=True)

                if resume_data['companies_worked_at'] is not None:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>
                        [+] Awesome! You have added your Previous Employers.</h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #fabc10;'>
                        [-] Please add your Previous Employers.</h4>''',
                        unsafe_allow_html=True)

                if resume_data['skills'] is not None:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>
                        [+] Awesome! You have added your Skills.</h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #fabc10;'>
                        [-] Please add your Skills.</h4>''',
                        unsafe_allow_html=True)

                if resume_data['years_of_experience'] is not None:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>
                        [+] Awesome! You have added your Years of Experience.</h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #fabc10;'>
                        [-] Please add your Years of Experience.</h4>''',
                        unsafe_allow_html=True)

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
                for percent_complete in range(resume_score):
                    score += 1
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1)
                st.success('**Your Resume Score: ' + str(score) + '**')

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
    layout='wide',
)

if st.session_state['connection_object'] is None:
    connection = db.set_connection()

if not db.check_connection():
    connection = db.set_connection()
cursor = db.set_cursor()

# db.init()

run()
