import streamlit as st


USERNAME = "admin"
PASSWORD = "password123"

def login():
    st.set_page_config(
        page_title="Login",
        page_icon="🔒",
        layout="centered"  
    )
    
 
    st.markdown("""
    <style>
    body {
        font-family: 'Times New Roman', serif;
    }
    .stApp {
        background: linear-gradient(to right, #4e54c8, #8f94fb);
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        width: 100%;
        margin: 10;
    }
    
    .login-container img {
        display: block;
        margin: 0 auto 1.5rem auto;
        
    }
    .login-container h2 {
        text-align: center;
        font-size: 2rem;
        margin-bottom: 1.5rem;
        font-weight: bold;
    }
    .login-container label {
        font-weight: bold;
        color: #4A5568;
    }
    .login-container .stTextInput, .login-container .stPasswordInput {
        margin-bottom: 5rem;
        border-radius: 5rem;
        border: 5px solid #E2E8F0;
    }
    .login-container button {
        display: block;
        width: 100%;
        background-color: #E2E8F0;
        color: black;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 9999px;
        border: none;
        cursor: pointer;
        margin-top: 1rem;
        transition: background-color 0.3s;
    }
    .login-container button:hover {
        background-color: #CBD5E0;
    }
    .login-container {
    background-color: white;
    padding: 2rem; 
    margin: 2% auto; /* Changed margin to 5% auto for better centering */
    border-radius: 1rem;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 950px; /* Changed width to 600px for better responsiveness */
    height: 550px; /* Changed height to auto to accommodate dynamic content */
    text-align: center;
    position: absolute; /* Changed position to relative to avoid absolute positioning issues */
    left: -20%;
    transform-translate(-50%, -50%);
    
}
    </style>
    """, unsafe_allow_html=True)

    
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<p align="center"><img src="https://static.thenounproject.com/png/1447099-200.png" alt="Image" style="width:100px;height:100px;"></p>', unsafe_allow_html=True)
        
        st.markdown("<h2>Login</h2>", unsafe_allow_html=True)
        
        username = st.text_input("Username", "")
        password = st.text_input("Password", type="password", value="")
        
        if st.button("Login"):
            if username == USERNAME and password == PASSWORD:
                st.session_state['logged_in'] = True
                st.success("Logged in successfully!")
                st.rerun()  
            else:
                st.error("Invalid username or password")
        
        st.markdown('</div>', unsafe_allow_html=True)

    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
