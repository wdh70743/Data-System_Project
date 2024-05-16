import random

import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app import get_db_connection

def create_account(name, email, address, region, department, password):
    dateCreated = str(datetime.now())
    connection = get_db_connection()
    Session = sessionmaker(bind=connection)
    session = Session()

    # Check if the email already exists in the database
    existing_user = session.execute(
        text("SELECT 1 FROM Users WHERE email = :email"),
        {'email': email}
    ).fetchone()
    if existing_user:
        session.close()  # Close the session if the email is already taken
        st.error("Email already exists. Please use a different email.")
        return False

    try:
        session.execute(
            text(
                "INSERT INTO Users (UserID, name, email, address, region, department, password, dateCreated) VALUES (:UserID, :name, :email, :address, :region, :department, :password, :dateCreated)"
            ),
            {'UserID': str(random.randint(50000, 17500000)),'name': name, 'email': email, 'address': address, 'region': region, 'department': department,
             'password': password, 'dateCreated': dateCreated}
        )
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        st.error(f"Failed to create account: {e}")
        return False
    finally:
        session.close()

def main():
    st.title("Create Account")
    with st.form("create_account_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        address = st.text_input("Address")
        region = st.text_input("Region")
        department = st.text_input("Department")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Create Account")

        if submit_button:
            with st.spinner("Creating account..."):
                if create_account(name, email, address, region, department, password):
                    st.success("Account created successfully!")
                    st.switch_page('app.py')
                else:
                    st.error("Failed to create account. Please check the inputs.")

if __name__ == '__main__':
    main()