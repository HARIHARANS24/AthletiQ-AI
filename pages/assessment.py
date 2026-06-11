import streamlit as st
from utils.helpers import render_sidebar_nav
from database.db import SessionLocal
from database.models import FitnessAssessment

if "user_id" not in st.session_state or st.session_state.user_id is None:
    st.warning("Please log in to view this page.")
    st.stop()

render_sidebar_nav()

st.title("📋 Fitness Assessment")
st.write("Complete this detailed assessment to get the most accurate AI-generated workout and diet plans.")

db = SessionLocal()
try:
    existing_assessment = db.query(FitnessAssessment).filter(FitnessAssessment.user_id == st.session_state.user_id).first()
    
    with st.form("assessment_form"):
        st.subheader("Current Fitness Level & Goals")
        col1, col2 = st.columns(2)
        with col1:
            fitness_level = st.selectbox("Current Fitness Level", ["Beginner", "Intermediate", "Advanced"], 
                                         index=["Beginner", "Intermediate", "Advanced"].index(existing_assessment.current_fitness_level) if existing_assessment and existing_assessment.current_fitness_level else 0)
            workout_experience = st.selectbox("Workout Experience", ["Less than 6 months", "6 months - 1 year", "1 - 3 years", "3+ years"],
                                             index=["Less than 6 months", "6 months - 1 year", "1 - 3 years", "3+ years"].index(existing_assessment.workout_experience) if existing_assessment and existing_assessment.workout_experience else 0)
        with col2:
            target_weight = st.number_input("Target Weight (kg)", min_value=20.0, max_value=300.0, value=existing_assessment.target_weight if existing_assessment and existing_assessment.target_weight else 70.0)
            goal_timeline = st.selectbox("Goal Timeline", ["1 month", "3 months", "6 months", "1 year"],
                                        index=["1 month", "3 months", "6 months", "1 year"].index(existing_assessment.goal_timeline) if existing_assessment and existing_assessment.goal_timeline else 1)
            
        st.subheader("Workout Preferences")
        col3, col4 = st.columns(2)
        with col3:
            workout_days = st.slider("Workout Days Per Week", 1, 7, value=existing_assessment.workout_days_per_week if existing_assessment and existing_assessment.workout_days_per_week else 3)
            workout_duration = st.slider("Workout Duration (minutes)", 15, 120, value=existing_assessment.workout_duration if existing_assessment and existing_assessment.workout_duration else 45, step=15)
        with col4:
            equipment_access = st.selectbox("Equipment Access", ["None (Bodyweight)", "Dumbbells/Kettlebells", "Resistance Bands", "Full Gym"],
                                           index=["None (Bodyweight)", "Dumbbells/Kettlebells", "Resistance Bands", "Full Gym"].index(existing_assessment.equipment_access) if existing_assessment and existing_assessment.equipment_access else 3)
            workout_frequency = st.selectbox("Current Daily Activity", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"],
                                            index=["Sedentary", "Lightly Active", "Moderately Active", "Very Active"].index(existing_assessment.workout_frequency) if existing_assessment and existing_assessment.workout_frequency else 1)
            
        st.subheader("Health & Diet")
        col5, col6 = st.columns(2)
        with col5:
            medical_conditions = st.text_area("Medical Conditions (e.g., Asthma, Knee Pain, None)", value=existing_assessment.medical_conditions if existing_assessment else "None")
            food_restrictions = st.text_area("Food Restrictions / Allergies", value=existing_assessment.food_restrictions if existing_assessment else "None")
        with col6:
            preferred_meals = st.selectbox("Diet Preference", ["Omnivore", "Vegetarian", "Vegan", "Keto", "Paleo"],
                                          index=["Omnivore", "Vegetarian", "Vegan", "Keto", "Paleo"].index(existing_assessment.preferred_meals) if existing_assessment and existing_assessment.preferred_meals in ["Omnivore", "Vegetarian", "Vegan", "Keto", "Paleo"] else 0)
            stress_level = st.selectbox("Stress Level", ["Low", "Moderate", "High"],
                                       index=["Low", "Moderate", "High"].index(existing_assessment.stress_level) if existing_assessment and existing_assessment.stress_level else 1)
            
        submitted = st.form_submit_button("Save Assessment")
        
        if submitted:
            if not existing_assessment:
                existing_assessment = FitnessAssessment(user_id=st.session_state.user_id)
                db.add(existing_assessment)
                
            existing_assessment.current_fitness_level = fitness_level
            existing_assessment.workout_experience = workout_experience
            existing_assessment.target_weight = target_weight
            existing_assessment.goal_timeline = goal_timeline
            existing_assessment.workout_days_per_week = workout_days
            existing_assessment.workout_duration = workout_duration
            existing_assessment.equipment_access = equipment_access
            existing_assessment.workout_frequency = workout_frequency
            existing_assessment.medical_conditions = medical_conditions
            existing_assessment.food_restrictions = food_restrictions
            existing_assessment.preferred_meals = preferred_meals
            existing_assessment.stress_level = stress_level
            db.commit()
            st.success("Assessment saved successfully! You can now generate AI plans.")
finally:
    db.close()
