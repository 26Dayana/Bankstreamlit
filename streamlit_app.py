import streamlit as st
from time import sleep
from navigation import make_sidebar
import mysql.connector
import plotly.express as px
import base64


make_sidebar()

st.title("Bank Marketing")

st.write("Please log in to continue")

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bank_marketing"
)

# Create a cursor
cursor = connection.cursor()

# Function to create users table if not exists
def create_users_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(100) NOT NULL
        )
    """)
    connection.commit()

create_users_table()

# Streamlit app
def main():
    
    #st.set_page_config(layout="wide")
    df = px.data.iris()

    
    def get_img_as_base64(file):
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()


    #img = get_img_as_base64(r".jpg")
    #data:image/png;base64,{img}
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://i.pinimg.com/736x/15/3a/45/153a4535df6cf2d2b106a558b750c486.jpg");
    background-size: cover;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: local;s
    }}


    .title {{
        font-size: 32px; /* Change this value to adjust the title size */
    }}
    </style>
    """
        
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        login()
    elif choice == "Register":
        register()

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username and password:
            if authenticate_user(username, password):   
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
                sleep(0.5)
                st.switch_page("pages/page1.py")   
            else:
                st.error("Invalid username or password")


    
def authenticate_user(username, password):
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    return True if result else False


        
def register():
    st.subheader("Register")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Register"):
        if new_username and new_password and confirm_password:
            if new_password == confirm_password:
                if register_user(new_username, new_password):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Username already exists")
            else:
                st.error("Passwords do not match")

def register_user(username, password):
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    if result:
        return False
    else:
        insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(insert_query, (username, password))
        connection.commit()
        return True

if __name__ == "__main__":
    main()
# Close cursor and connection
cursor.close()
connection.close()