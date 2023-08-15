import pymysql
import streamlit as st
import pandas as pd


def create_user_data_table():
    print("Creating user data table...")

    # 'user_data'
    user_data_table = st.secrets.connections.mysql.user_data
    user_data_table_sql = "CREATE TABLE IF NOT EXISTS " + user_data_table + """
                    (Timestamp VARCHAR(50) NOT NULL,
                    Name VARCHAR(100) NOT NULL,
                     Email VARCHAR(50) NOT NULL,
                     LinkedIn VARCHAR(50) NOT NULL,
                     Contact VARCHAR(15) NOT NULL,
                     Skills VARCHAR(300) NOT NULL,
                     Resume_Score VARCHAR(8) NOT NULL);
                    """
    cursor.execute(user_data_table_sql)


def insert_user_data(user_data_table, timestamp, name, email, linkedin, phone, skills, resume_score):
    print("Inserting values in user data table...")

    insert_sql = "insert into " + user_data_table + """
    values (%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (timestamp, name, email, linkedin, phone, skills, resume_score)

    cursor.execute(insert_sql, rec_values)
    connection.commit()


def get_user_data(user_data_table):
    print("Getting user data table...")

    cursor.execute('SELECT * FROM ' + user_data_table)
    user_data = cursor.fetchall()

    user_df = pd.DataFrame(user_data, columns=['Timestamp', 'Name', 'Email', 'LinkedIn',
                                               'Phone', 'Skills', 'Resume Score'
                                               ])
    return user_df


def create_listing_data_table():
    print("Creating listing data table...")

    # 'listing_data'
    listing_data_table = st.secrets.connections.mysql.listing_table
    listing_data_table_sql = "CREATE TABLE IF NOT EXISTS " + listing_data_table + """
                                        (Job_Description VARCHAR(250) NOT NULL,
                                         Job_Responsibilities VARCHAR(250) NOT NULL,
                                         Job_Skills VARCHAR(250) NOT NULL);
                                        """
    cursor.execute(listing_data_table_sql)


def insert_listing_data(listing_data_table, job_desc, job_res, job_skills):
    print("Inserting values in listing data table...")

    insert_sql = "insert into " + listing_data_table + """
        values (%s,%s,%s)"""
    rec_values = (job_desc, job_res, job_skills)

    cursor.execute(insert_sql, rec_values)
    connection.commit()
    # conn.query(insert_sql % rec_values)


def get_listing_data(listing_data_table):
    print("Getting listing data table...")

    cursor.execute('SELECT * FROM ' + listing_data_table)
    listing_data = cursor.fetchall()
    # listing_data = conn.query('SELECT * FROM ' + listing_data_table)
    listing_df = pd.DataFrame(listing_data, columns=['Job Description', 'Job Responsibilities', 'Job Skills'])
    return listing_df


def create_database():
    print("Creating database...")

    # "HRM_DATABASE"
    db = st.secrets.connections.mysql.database
    db_sql = "CREATE DATABASE IF NOT EXISTS " + db + ";"
    cursor.execute(db_sql)


def set_database():
    print("Selecting database...")

    db = st.secrets.connections.mysql.database
    connection.select_db(db)


def set_connection():
    print("Setting up connection to server...")

    global connection
    connection = pymysql.connect(host=st.secrets.connections.mysql.host,
                                 user=st.secrets.connections.mysql.username,
                                 password=st.secrets.connections.mysql.password)

    if connection.open:
        print("Connection Established.")
    else:
        print("Some error occurred in establishing a connection.")

    global cursor
    cursor = connection.cursor()
    set_database()
    return connection, cursor
