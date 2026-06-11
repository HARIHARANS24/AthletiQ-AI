import streamlit as st
import pandas as pd
from datetime import datetime
from utils.helpers import render_sidebar_nav
from database.db import SessionLocal
from database.models import ProgressLog

if "user_id" not in st.session_state or st.session_state.user_id is None:
    st.warning("Please log in to view this page.")
    st.stop()

render_sidebar_nav()

st.title("📈 Progress Tracker")

db = SessionLocal()
try:
    with st.expander("➕ Log New Entry", expanded=True):
        with st.form("progress_form"):
            date = st.date_input("Date", datetime.today())
            col1, col2, col3 = st.columns(3)
            with col1:
                weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=70.0)
                calories = st.number_input("Calories Consumed", min_value=0, max_value=10000, value=2000)
            with col2:
                water = st.number_input("Water Intake (L)", min_value=0.0, max_value=10.0, value=2.0, step=0.1)
                steps = st.number_input("Steps", min_value=0, max_value=100000, value=8000)
            with col3:
                sleep = st.number_input("Sleep Hours", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
                workout_completed = st.checkbox("Workout Completed today?")
                
            st.subheader("Measurements (Optional)")
            col4, col5 = st.columns(2)
            with col4:
                chest = st.number_input("Chest (cm)", value=0.0)
                waist = st.number_input("Waist (cm)", value=0.0)
            with col5:
                arms = st.number_input("Arms (cm)", value=0.0)
                thighs = st.number_input("Thighs (cm)", value=0.0)
                
            submitted = st.form_submit_button("Save Progress")
            
            if submitted:
                new_log = ProgressLog(
                    user_id=st.session_state.user_id,
                    date=date,
                    weight=weight,
                    calories_consumed=calories,
                    water_intake=water,
                    steps=steps,
                    sleep_hours=sleep,
                    workout_completed=workout_completed,
                    chest=chest if chest > 0 else None,
                    waist=waist if waist > 0 else None,
                    arms=arms if arms > 0 else None,
                    thighs=thighs if thighs > 0 else None
                )
                db.add(new_log)
                db.commit()
                st.success("Progress logged successfully!")
                st.rerun()

    st.markdown("---")
    st.subheader("Your Progress History")
    
    logs = db.query(ProgressLog).filter(ProgressLog.user_id == st.session_state.user_id).order_by(ProgressLog.date.desc()).all()
    if logs:
        data = []
        for log in logs:
            data.append({
                "Date": log.date.strftime("%Y-%m-%d"),
                "Weight (kg)": log.weight,
                "Calories": log.calories_consumed,
                "Water (L)": log.water_intake,
                "Steps": log.steps,
                "Sleep (hrs)": log.sleep_hours,
                "Workout Done": "Yes" if log.workout_completed else "No"
            })
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No progress logs yet. Start tracking above!")
finally:
    db.close()
