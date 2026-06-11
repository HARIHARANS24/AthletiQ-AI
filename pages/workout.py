import streamlit as st
import json
from utils.helpers import render_sidebar_nav
from database.db import SessionLocal
from database.models import User, FitnessAssessment
from services.gemini_service import generate_workout_plan
from services.workout_service import save_workout_plan, get_workout_plan

if "user_id" not in st.session_state or st.session_state.user_id is None:
    st.warning("Please log in to view this page.")
    st.stop()

render_sidebar_nav()

st.title("🏋️‍♂️ AI Workout Planner")

db = SessionLocal()
try:
    user = db.query(User).filter(User.id == st.session_state.user_id).first()
    assessment = db.query(FitnessAssessment).filter(FitnessAssessment.user_id == st.session_state.user_id).first()
finally:
    db.close()

if not user or not user.height or not user.weight:
    st.warning("Please update your Profile with your height and weight first.")
    st.stop()
    
if not assessment:
    st.warning("Please complete your Fitness Assessment first to get a personalized plan.")
    st.stop()

existing_plan = get_workout_plan(st.session_state.user_id)

col1, col2 = st.columns([3, 1])
with col1:
    st.write("Generate a personalized weekly workout plan using AI based on your profile and fitness assessment.")
with col2:
    if st.button("Generate New Plan", type="primary"):
        with st.spinner("Our AI is creating your personalized plan... This may take a few seconds."):
            user_data = {
                "age": user.age,
                "gender": user.gender,
                "height": user.height,
                "weight": user.weight,
                "goal": user.fitness_goal or f"Target weight: {assessment.target_weight}kg",
                "experience": assessment.workout_experience,
                "equipment": assessment.equipment_access,
                "days": assessment.workout_days_per_week
            }
            try:
                new_plan = generate_workout_plan(user_data)
                save_workout_plan(st.session_state.user_id, new_plan)
                existing_plan = new_plan
                st.success("Plan generated successfully!")
            except Exception as e:
                st.error(f"Error generating plan: {e}")

if existing_plan:
    st.markdown("---")
    st.subheader("Your Weekly Workout Schedule")
    
    tabs = st.tabs(list(existing_plan.keys()))
    
    for i, (day, day_plan) in enumerate(existing_plan.items()):
        with tabs[i]:
            st.markdown(f"### {day_plan.get('WorkoutType', 'Rest Day')}")
            
            if day_plan.get('WorkoutType', '').lower() != 'rest':
                if day_plan.get('Warmup'):
                    st.info(f"**Warmup:** {day_plan['Warmup']}")
                    
                if day_plan.get('Exercises'):
                    for ex in day_plan['Exercises']:
                        with st.expander(f"💪 {ex.get('Exercise', 'Exercise')}"):
                            st.write(f"**Sets:** {ex.get('Sets', '-')} | **Reps:** {ex.get('Reps', '-')} | **Rest:** {ex.get('Rest', '-')}")
                            
                if day_plan.get('Cooldown'):
                    st.success(f"**Cooldown:** {day_plan['Cooldown']}")
                    
                if day_plan.get('EstimatedCaloriesBurned'):
                    st.metric("Estimated Calories Burned", f"{day_plan['EstimatedCaloriesBurned']} kcal")
            else:
                st.write("Enjoy your rest day! Proper recovery is crucial for progress.")
