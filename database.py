import pymysql
import streamlit as st
import pandas as pd


def create_database():
    # "HRM_DATABASE"
    db = st.secrets.connections.mysql.database
    db_sql = "CREATE DATABASE IF NOT EXISTS " + db + ";"
    cursor.execute(db_sql)
    connection.select_db(db)

    create_database()
    create_user_data_table()
    create_listing_data_table()


def create_user_data_table():
    # 'user_data'
    user_data_table = st.secrets.connections.mysql.user_data
    user_data_table_sql = "CREATE TABLE IF NOT EXISTS " + user_data_table + """
                    (Timestamp VARCHAR(50) NOT NULL,
                    Name VARCHAR(100) NOT NULL,
                     Email VARCHAR(50) NOT NULL,
                     LinkedIn VARCHAR(50) NOT NULL,
                     Contact VARCHAR(15) NOT NULL,
                     Skills VARCHAR(300) NOT NULL
                     Resume_Score VARCHAR(8) NOT NULL);
                    """
    cursor.execute(user_data_table_sql)


def create_listing_data_table():
    # 'listing_data'
    listing_data_table = st.secrets.connections.mysql.listing_table
    listing_data_table_sql = "CREATE TABLE IF NOT EXISTS " + listing_data_table + """
                                        (Job_Description VARCHAR(250) NOT NULL,
                                         Job_Responsibilities VARCHAR(250) NOT NULL,
                                         Job_Skills VARCHAR(250) NOT NULL);
                                        """
    cursor.execute(listing_data_table_sql)


def insert_user_data(user_data_table, timestamp, name, email, linkedin, phone, skills, resume_score):
    insert_sql = "insert into " + user_data_table + """
    values (%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (name, email, linkedin, phone, resume_score, timestamp, skills)

    cursor.execute(insert_sql, rec_values)
    connection.commit()
    # conn.query(insert_sql % rec_values)


def get_user_data(user_data_table):
    cursor.execute('SELECT * FROM ' + user_data_table)
    user_data = cursor.fetchall()
    # user_data = conn.query('SELECT * FROM ' + user_data_table)

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
    # conn.query(insert_sql % rec_values)


def get_listing_data(listing_data_table):
    cursor.execute('SELECT * FROM ' + listing_data_table)
    listing_data = cursor.fetchall()
    # listing_data = conn.query('SELECT * FROM ' + listing_data_table)
    listing_df = pd.DataFrame(listing_data, columns=['Job Description', 'Job Responsibilities', 'Job Skills'])
    return listing_df


def set_connection():
    connection = pymysql.connect(host=st.secrets.connections.mysql.host,
                                 user=st.secrets.connections.mysql.username,
                                 password=st.secrets.connections.mysql.password)
    cursor = connection.cursor()
    return connection, cursor


if __name__ == '__main__':
    connection, cursor = set_connection()