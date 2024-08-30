import streamlit as st

# Constants for username and password
USERNAME = "admin"
PASSWORD = "password123"

def login():
    st.set_page_config(
        page_title="Login",
        page_icon="🔒",
        layout="wide"  # Use wide layout to allow sidebar placement
    )
    
    # Add custom CSS to style the login page
    st.markdown(
        """
        <style>
        .login-title {
            color: #007BFF; /* Blue color for the title */
            font-size: 2em;
            margin-bottom: 20px;
            text-align: center;
        }
        .login-container {
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
            background-color: rgba(255, 255, 255, 0.9);
        }
        .login-form input {
            margin: 10px 0;
            width: 100%;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        .login-form button {
            background-color: #007BFF;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        .login-form button:hover {
            background-color: #0056b3;
        }
        .login-form h2 {
            margin-bottom: 20px;
            color: #333;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Login form in the sidebar
    st.sidebar.title("Login to G.A.R.V.I.S")
    
    username = st.sidebar.text_input("Username", "")
    password = st.sidebar.text_input("Password", type="password", value="")
    
    if st.sidebar.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state['logged_in'] = True
            st.sidebar.success("Logged in successfully!")
            st.experimental_rerun()  # Refresh to go back to the main application
        else:
            st.sidebar.error("Invalid username or password")

    # Initialize session state if not set
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False    
