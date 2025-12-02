import streamlit as st
import sqlite3


# -----------------------------
# Database Functions
# -----------------------------
def create_usertable():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT
        )
        ''')
    conn.commit()
    conn.close()


def add_userdata(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users(username, password) VALUES (?,?)', (username, password))
    conn.commit()
    conn.close()


def login_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    data = c.fetchall()
    conn.close()
    return data


def update_password(username, new_password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
    conn.commit()
    conn.close()


def check_user_exists(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    data = c.fetchall()
    conn.close()
    return data


# -----------------------------
# Streamlit App
# -----------------------------
def main():
    st.title("Login & Registration System")

    create_usertable()

    menu = ["Home", "Login", "SignUp", "Forgot Password"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Welcome to the Home Page")
        st.write("Please use the left side menu to Login or Register.")

    elif choice == "Login":
        st.subheader("Login Section")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            result = login_user(username, password)
            if result:
                st.success(f"Welcome {username}!")
            else:
                st.error("Incorrect Username or Password")

    elif choice == "SignUp":
        st.subheader("Create a New Account")

        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("SignUp"):
            if new_password == confirm_password:
                add_userdata(new_user, new_password)
                st.success("Account created successfully!")
                st.info("Go to Login Menu to log in.")
            else:
                st.error("Passwords do not match")

    elif choice == "Forgot Password":
        st.subheader("Reset Your Password")

        username = st.text_input("Enter your username")

        if st.button("Check User"):
            if check_user_exists(username):
                st.success("User found!")

                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")

                if st.button("Reset Password"):
                    if new_password == confirm_password:
                        update_password(username, new_password)
                        st.success("Password updated successfully!")
                    else:
                        st.error("Passwords do not match")
            else:
                st.error("Username does not exist")


if __name__ == '__main__':
    main()
