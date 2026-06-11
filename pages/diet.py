import streamlit as st
import json
from utils.helpers import render_sidebar_nav
from database.db import SessionLocal
from database.models import User, FitnessAssessment
from services.gemini_service import generate_meal_plan
from services.diet_service import save_diet_plan, get_diet_plan

if "user_id" not in st.session_state or st.session_state.user_id is None:
    st.warning("Please log in to view this page.")
    st.stop()

render_sidebar_nav()

st.title("🥗 AI Diet Planner")

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

existing_plan = get_diet_plan(st.session_state.user_id)

col1, col2 = st.columns([3, 1])
with col1:
    st.write("Generate a personalized daily meal plan based on your dietary preferences and fitness goals.")
with col2:
    if st.button("Generate New Plan", type="primary"):
        with st.spinner("Our AI is creating your personalized meal plan..."):
            user_data = {
                "age": user.age,
                "gender": user.gender,
                "height": user.height,
                "weight": user.weight,
                "goal": user.fitness_goal or f"Target weight: {assessment.target_weight}kg",
                "activity_level": assessment.workout_frequency,
                "diet": assessment.preferred_meals
            }
            try:
                new_plan = generate_meal_plan(user_data)
                save_diet_plan(st.session_state.user_id, new_plan)
                existing_plan = new_plan
                st.success("Diet plan generated successfully!")
            except Exception as e:
                st.error(f"Error generating plan: {e}")

if existing_plan:
    st.markdown("---")
    st.subheader("Your Daily Nutrition Plan")
    
    col_mac1, col_mac2, col_mac3 = st.columns(3)
    macros = existing_plan.get("DailyMacros", {})
    with col_mac1:
        st.metric("Target Calories", f"{existing_plan.get('TargetCalories', '-')} kcal")
    with col_mac2:
        st.metric("Maintenance Calories", f"{existing_plan.get('MaintenanceCalories', '-')} kcal")
    with col_mac3:
        st.markdown(f"**Protein:** {macros.get('Protein', '-')} | **Carbs:** {macros.get('Carbs', '-')} | **Fats:** {macros.get('Fats', '-')}")
        
    st.markdown("### Meals")
    meals = existing_plan.get("Meals", {})
    for meal_name, meal_details in meals.items():
        with st.expander(f"🍽️ {meal_name} - {meal_details.get('Calories', '-')} kcal"):
            items = meal_details.get("Items", [])
            st.write("**Items:** " + ", ".join(items))
            st.write(f"**Protein:** {meal_details.get('Protein', '-')} | **Carbs:** {meal_details.get('Carbs', '-')} | **Fats:** {meal_details.get('Fats', '-')}")
