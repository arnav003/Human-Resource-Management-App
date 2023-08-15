import pymysql
import streamlit as st
import pandas as pd


def create_user_data_table():
    print("Creating user data table...")

    if not check_connection():
        set_connection()

    try:
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
        print("Created user data table.")
    except pymysql.err.OperationalError:
        print("Some error occurred. Unable to create user data table.")


def insert_user_data(user_data_table, timestamp, name, email, linkedin, phone, skills, resume_score):
    print("Inserting values in user data table...")

    if not check_connection():
        set_connection()

    try:
        insert_sql = "insert into " + user_data_table + """
        values (%s,%s,%s,%s,%s,%s,%s)"""
        rec_values = (timestamp, name, email, linkedin, phone, skills, resume_score)

        cursor.execute(insert_sql, rec_values)
        st.session_state['connection_object'].commit()
        print("Values inserted in user data table.")
    except pymysql.err.OperationalError:
        print("Some error occurred. Unable to insert values in user data table.")


def get_user_data(user_data_table):
    print("Getting user data table...")

    if not check_connection():
        set_connection()

    try:
        cursor.execute('SELECT * FROM ' + user_data_table)
        user_data = cursor.fetchall()

        user_df = pd.DataFrame(user_data, columns=['Timestamp', 'Name', 'Email', 'LinkedIn',
                                                   'Phone', 'Skills', 'Resume Score'
                                                   ])
        print("Fetched user data table.")
        return user_df
    except pymysql.err.OperationalError:
        print("Some error occurred. Unable to fetch user data table.")
        return None


def create_listing_data_table():
    print("Creating listing data table...")

    if not check_connection():
        set_connection()

    try:
        # 'listing_data'
        listing_data_table = st.secrets.connections.mysql.listing_table
        listing_data_table_sql = "CREATE TABLE IF NOT EXISTS " + listing_data_table + """
                                            (Job_Description VARCHAR(250) NOT NULL,
                                             Job_Responsibilities VARCHAR(250) NOT NULL,
                                             Job_Skills VARCHAR(250) NOT NULL);
                                            """
        cursor.execute(listing_data_table_sql)
        print("Created listing data table.")
    except pymysql.err.OperationalError:
        print("Some error occurred. Unable to create listing data table.")


def insert_listing_data(listing_data_table, job_desc, job_res, job_skills):
    print("Inserting values in listing data table...")

    if not check_connection():
        set_connection()

    try:
        insert_sql = "insert into " + listing_data_table + """
            values (%s,%s,%s)"""
        rec_values = (job_desc, job_res, job_skills)

        cursor.execute(insert_sql, rec_values)
        st.session_state['connection_object'].commit()
        print("Values inserted in listing data table.")
    except pymysql.err.OperationalError:
        print("Some error occurred. Unable to insert values in listing data table.")


def get_listing_data(listing_data_table):
    print("Getting listing data table...")

    if not check_connection():
        set_connection()

    try:
        cursor.execute('SELECT * FROM ' + listing_data_table)
        listing_data = cursor.fetchall()
        listing_df = pd.DataFrame(listing_data, columns=['Job Description', 'Job Responsibilities', 'Job Skills'])
        print("Fetched listing data table.")
        return listing_df
    except pymysql.err.OperationalError:
        print("Some error occurred. Unable to fetch listing data table.")
        return None


def create_database():
    print("Creating database...")

    if not check_connection():
        set_connection()

    try:
        # "HRM_DATABASE"
        db = st.secrets.connections.mysql.database
        db_sql = "CREATE DATABASE IF NOT EXISTS " + db + ";"
        cursor.execute(db_sql)
        print("Database created.")
    except pymysql.err.OperationalError:
        print("Some error occurred. Unable to create database.")


def set_database():
    print("Selecting database...")

    if not check_connection():
        set_connection()

    try:
        db = st.secrets.connections.mysql.database
        st.session_state['connection_object'].select_db(db)
        print("Database selected.")
    except pymysql.err.OperationalError:
        print("Some error occurred. Unable to select database.")


def set_connection():
    print("Setting up connection to server...")

    global connection
    connection = pymysql.connect(host=st.secrets.connections.mysql.host,
                                 user=st.secrets.connections.mysql.username,
                                 password=st.secrets.connections.mysql.password)

    if connection.open:
        print("Connection Established.")
        st.session_state['connection_object'] = connection
        set_database()
        return connection
    else:
        print("Some error occurred. Unable to establish a connection.")
        return None


def set_cursor():
    if not check_connection:
        set_connection()

    global cursor
    cursor = st.session_state['connection_object'].cursor()

    return cursor


def check_connection():
    if st.session_state['connection_object'].open:
        return True
    else:
        print("Connection broken. Retrying...")
        return False
