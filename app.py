import time

import numpy as np
import pandas as pd
import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, URL, text
from dotenv import load_dotenv
import os
load_dotenv()

def get_db_connection():
    connection_url = URL.create(
        "mssql+pyodbc",
        username=os.environ.get('DB_USERNAME'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DATABASE'),
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "encrypt": "yes",
            "TrustServerCertificate": "no",
            "Connection Timeout": "30"
        }
    )
    engine = create_engine(connection_url)
    return engine

def verify_user(email, password, connection):
    Session = sessionmaker(bind=connection)
    session = Session()
    user = session.execute(
        text(
        "SELECT * FROM Users WHERE email = :email AND password = :password"),
        {'email': email, 'password': password}
    ).fetchone()
    session.close()
    return user

def logout():
    if 'is_authenticated' in st.session_state:
        del st.session_state['is_authenticated']
    if 'user_details' in st.session_state:
        del st.session_state['user_details']
    st.experimental_rerun()

def main():
    st.title('Login Page')

    if 'is_authenticated' in st.session_state and st.session_state['is_authenticated']:
        _LOREM_IPSUM = "Welcome, you are already logged in."
        def stream_data():
            for word in _LOREM_IPSUM.split(" "):
                yield word + " "
                time.sleep(0.2)
        st.write_stream(stream_data)

        user_details = st.session_state.get('user_details', {})
        st.json(user_details)  # Display user details in a JSON format or format as needed
        if st.button('Logout'):
            logout()

    else:
        username = st.text_input('Email')
        password = st.text_input('Password', type='password')

        if st.button('Register'):
            st.switch_page('pages/register.py')

        if st.button('Login'):
            with st.spinner('Logging in...'):
                connection = get_db_connection()
                user = verify_user(username, password, connection)
            if user:
                st.success('Login Successful!')
                print(user)
                st.session_state['is_authenticated'] = True
                st.session_state['user_details'] = {
                    "UserID": user[0],
                    "Name": user[1],
                    "Email": user[2],
                    "Address": user[3],
                    "Region": user[4],
                    "Department": user[5],
                    "createdAt": user[7]
                }
                st.switch_page('pages/visualisation.py')
            else:
                st.error('Login Failed. Check your username or password.')

if __name__ == '__main__':
    main()