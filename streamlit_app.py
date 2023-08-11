import streamlit as st
import pandas as pd
import base64
import time
import datetime
import ResumeParser
import pymysql
from PIL import Image


@st.cache_resource
def get_data(save_image_path):
    text = ResumeParser.get_text_from_pdf(save_image_path)
    data = ResumeParser.extract_data(text)
    return data


def print_list_with_text(ls, text, print_list=True):
    out = ""
    if print_list:
        col1, col2 = st.columns([1, 5])
        col1.write(f'{text}: ')
    if ls is not None:
        for ele in ls:
            out = out + ele + "\n"
            if print_list:
                col2.text(ele)
    else:
        out = f"{text} not found."
        if print_list:
            col2.error(out)

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


def insert_user_data(user_data_table, name, email, linkedin, phone, resume_score, timestamp, skills):
    insert_sql = "insert into " + user_data_table + """
    values (%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (name, email, linkedin, phone, resume_score, timestamp, skills)

    cursor.execute(insert_sql, rec_values)
    connection.commit()


def get_user_data(user_data_table):
    cursor.execute('SELECT * FROM ' + user_data_table)
    user_data = cursor.fetchall()
    user_df = pd.DataFrame(user_data, columns=['Name', 'Email', 'LinkedIn',
                                               'Phone', 'Resume Score', 'Timestamp',
                                               'Skills'])
    return user_df


def insert_listing_data(listing_data_table, job_desc, job_res, job_skills):
    insert_sql = "insert into " + listing_data_table + """
        values (%s,%s,%s)"""
    rec_values = (job_desc, job_res, job_skills)

    cursor.execute(insert_sql, rec_values)
    connection.commit()


def get_listing_data(listing_data_table):
    cursor.execute('SELECT * FROM ' + listing_data_table)
    listing_data = cursor.fetchall()
    listing_df = pd.DataFrame(listing_data, columns=['Job Description', 'Job Responsibilities', 'Job Skills'])
    return listing_df


def run():
    col1, col2 = st.columns([1, 6])
    img = Image.open('Resources/Images/Logo.png')
    img = img.resize((75, 75))
    col1.image(img)
    col2.title("Human Resource Management")

    st.sidebar.markdown("# Choose User")
    activities = ["User", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)

    db = "HRM_DATABASE"
    db_sql = """CREATE DATABASE IF NOT EXISTS """ + db + ';'
    cursor.execute(db_sql)
    connection.select_db(db)

    user_data_table = 'user_data'
    # table_sql = "CREATE TABLE IF NOT EXISTS " + user_data_table + """
    #                 (Timestamp VARCHAR(50) NOT NULL,
    #                 Name VARCHAR(100) NOT NULL,
    #                  Email VARCHAR(50) NOT NULL,
    #                  LinkedIn VARCHAR(50) NOT NULL,
    #                  Contact VARCHAR(15) NOT NULL,
    #                  Skills VARCHAR(300) NOT NULL
    #                  Resume_Score VARCHAR(8) NOT NULL);
    #                 """
    # cursor.execute(table_sql)
    if choice == 'User':
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        if pdf_file is not None:
            save_image_path = './Uploaded Resumes/' + pdf_file.name
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            resume_data = get_data(save_image_path)

            if resume_data:
                st.header("Hello, " + print_list_with_text(resume_data['name'], "Name", print_list=False))

                show_pdf(save_image_path)

                with st.expander("Extracted Details"):
                    name = print_list_with_text(resume_data['name'], "Name")
                    email = print_list_with_text(resume_data['email'], "Email")
                    phone = print_list_with_text(resume_data['phone number'], "Phone Number")
                    linkedin = print_list_with_text(resume_data['linkedin'], "LinkedIn")
                    skills = print_list_with_text(resume_data["skills"], "Skills")
                    degree = print_list_with_text(resume_data["degree"], "Degree")
                    year_of_graduation = print_list_with_text(resume_data["year of graduation"], "Year of Graduation")
                    university = print_list_with_text(resume_data["university"], "University")
                    certification = print_list_with_text(resume_data["certification"], "Certification")
                    awards = print_list_with_text(resume_data["awards"], "Awards")
                    worked_as = print_list_with_text(resume_data["worked as"], "Worked As")
                    companies_worked_at = print_list_with_text(resume_data["companies worked at"],
                                                               "Companies Worked At")
                    years_of_experience = print_list_with_text(resume_data["years of experience"],
                                                               "Years of Experience")
                    language = print_list_with_text(resume_data["language"], "Language")

                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date + '_' + cur_time)

                st.subheader("**Resume Analysis**")
                resume_score = 0

                if resume_data['degree'] is not None or resume_data['university'] is not None:
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

                if resume_data['worked as'] is not None:
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

                if resume_data['companies worked at'] is not None:
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

                if resume_data['years of experience'] is not None:
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

                insert_user_data(user_data_table, name, email, linkedin, phone, str(resume_score), timestamp, skills)

                connection.commit()
            else:
                st.error('Something went wrong..')
    else:
        ## Admin Side
        st.markdown('### Welcome to Admin Portal')

        if st.session_state['admin_logged_in'] == False:
            ad_user = st.text_input("Username")
            ad_password = st.text_input("Password", type='password')
            if st.button('Login'):
                if ad_user == 'admin' and ad_password == '123456':
                    st.session_state['admin_logged_in'] = True
                else:
                    st.error("Wrong ID or Password.")
        else:
            st.success("Welcome Admin")

            st.header("User Data")
            user_data_df = get_user_data(user_data_table)
            st.dataframe(user_data_df)

            st.markdown(get_table_download_link(user_data_df, "user_data.csv", "Download User Data"),
                        unsafe_allow_html=True)

            listing_data_table = 'listing_data'
            table_sql = "CREATE TABLE IF NOT EXISTS " + listing_data_table + """
                                                (Job_Description VARCHAR(250) NOT NULL,
                                                 Job_Responsibilities VARCHAR(250) NOT NULL,
                                                 Job_Skills VARCHAR(250) NOT NULL);
                                                """
            cursor.execute(table_sql)

            st.header("Listing Data")
            listing_data_df = get_listing_data(listing_data_table)
            st.dataframe(listing_data_df)

            st.markdown(get_table_download_link(listing_data_df, "listing_data.csv", "Download Listing Data"),
                        unsafe_allow_html=True)

            with st.expander(label="Add new listing", expanded=False):
                job_desc = st.text_input("Job Description")
                job_res = st.text_input("Job Responsibilities")
                job_skills = st.text_input("Job Skills")

                if st.button('Add listing'):
                    insert_listing_data(listing_data_table, job_desc, job_res, job_skills)
                    cursor.execute(table_sql)


if 'admin_logged_in' not in st.session_state:
    st.session_state['admin_logged_in'] = False

st.set_page_config(
    page_title="Human Resource Management Portal",
    page_icon='./Resources/Images/Logo.png',
)

connection = pymysql.connect(host='localhost', user='root', password='12345678')
cursor = connection.cursor()

run()
