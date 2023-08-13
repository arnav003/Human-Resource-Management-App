import pymysql
import streamlit as st

connection = pymysql.connect(host=st.secrets.connections.mysql.host,
                             user=st.secrets.connections.mysql.username,
                             password=st.secrets.connections.mysql.password)
cursor = connection.cursor()

#"HRM_DATABASE"
db = st.secrets.connections.mysql.database
db_sql = """CREATE DATABASE IF NOT EXISTS """ + db + ';'
cursor.execute(db_sql)
connection.select_db(db)

#'user_data'
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