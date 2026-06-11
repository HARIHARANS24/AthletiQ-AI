import streamlit as st
from utils.helpers import render_sidebar_nav
from database.db import SessionLocal
from database.models import User

if "user_id" not in st.session_state or st.session_state.user_id is None:
    st.warning("Please log in to view this page.")
    st.stop()

render_sidebar_nav()

st.title("👤 User Profile")

db = SessionLocal()
try:
    user = db.query(User).filter(User.id == st.session_state.user_id).first()
    
    with st.form("profile_form"):
        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name", value=user.full_name)
            age = st.number_input("Age", min_value=10, max_value=120, value=user.age if user.age else 25)
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(user.gender) if user.gender in ["Male", "Female", "Other"] else 0)
            
        st.subheader("Body Metrics")
        col3, col4 = st.columns(2)
        with col3:
            height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=user.height if user.height else 170.0)
        with col4:
            weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=user.weight if user.weight else 70.0)
            
        submitted = st.form_submit_button("Save Profile")
        
        if submitted:
            user.full_name = full_name
            user.age = age
            user.gender = gender
            user.height = height
            user.weight = weight
            db.commit()
            st.success("Profile updated successfully!")
            st.rerun()
finally:
    db.close()
