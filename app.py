import streamlit as st
import os
from dotenv import load_dotenv
from database.db import init_db

# Load environment variables
load_dotenv()

# Configure the Streamlit application
st.set_page_config(
    page_title="AI Fitness Planner",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize the database on startup
@st.cache_resource
def setup_database():
    init_db()

try:
    setup_database()
except Exception as e:
    st.error(f"Failed to initialize database: {e}")

# Authentication state management
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None

# Routing & Navigation
if st.session_state.user_id is None:
    st.sidebar.title("Login / Sign Up")
    st.title("Welcome to AI Fitness Planner 🏋️‍♂️")
    st.write("Please log in or sign up to access your personalized dashboard.")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", type="primary"):
            from services.auth_service import login_user
            user = login_user(login_email, login_password)
            if user:
                st.session_state.user_id = user.id
                st.session_state.username = user.full_name
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid email or password.")
                
    with tab2:
        st.subheader("Create an Account")
        reg_name = st.text_input("Full Name")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        if st.button("Sign Up", type="primary"):
            from services.auth_service import register_user
            success, msg = register_user(reg_name, reg_email, reg_password)
            if success:
                st.success("Registration successful! Please log in.")
            else:
                st.error(msg)
else:
    # Sidebar navigation when logged in
    st.sidebar.title(f"Welcome, {st.session_state.username}!")
    if st.sidebar.button("Logout"):
        st.session_state.user_id = None
        st.session_state.username = None
        st.rerun()
        
    st.sidebar.markdown("---")
    st.sidebar.info("Select a page above to navigate.")
    
    st.title(f"Hello, {st.session_state.username}! 👋")
    st.write("Select a page from the sidebar to get started.")
    
    st.info("Head over to the **Dashboard** to view your stats, or update your **Profile** to get personalized recommendations.")
