import streamlit as st
from utils.helpers import render_sidebar_nav, create_bmi_gauge
from services.analytics_service import get_dashboard_metrics

if "user_id" not in st.session_state or st.session_state.user_id is None:
    st.warning("Please log in to view this page.")
    st.stop()

render_sidebar_nav()

st.title("📊 Dashboard")

metrics = get_dashboard_metrics(st.session_state.user_id)
from database.db import SessionLocal
from database.models import User
from utils.bmi import calculate_bmi, get_bmi_category

db = SessionLocal()
try:
    user = db.query(User).filter(User.id == st.session_state.user_id).first()
    bmi = calculate_bmi(metrics['current_weight'], user.height / 100 if user and user.height else 0)
    bmi_category = get_bmi_category(bmi)
finally:
    db.close()

st.header("Quick Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Current Weight", value=f"{metrics['current_weight'] or 0} kg", 
              delta=f"Target: {metrics['target_weight']} kg" if metrics['target_weight'] else None)
with col2:
    st.metric(label="BMI Category", value=bmi_category)
with col3:
    st.metric(label="Daily Calories", value=f"{metrics['latest_calories']} kcal")
with col4:
    st.metric(label="Water Intake", value=f"{metrics['latest_water']} L")

st.markdown("---")
st.subheader("Your BMI Analysis")

fig = create_bmi_gauge(bmi)
st.plotly_chart(fig, use_container_width=True)

st.info("Tip: Update your Progress Tracker daily to keep this dashboard accurate!")

from reports.pdf_generator import generate_pdf_report
from services.workout_service import get_workout_plan
from services.diet_service import get_diet_plan
from database.models import FitnessAssessment

st.markdown("---")
st.subheader("📄 Generate Report")
if st.button("Download Full Fitness & Diet Report", type="primary"):
    with st.spinner("Generating PDF..."):
        workout_plan = get_workout_plan(st.session_state.user_id)
        diet_plan = get_diet_plan(st.session_state.user_id)
        
        db = SessionLocal()
        try:
            assessment = db.query(FitnessAssessment).filter(FitnessAssessment.user_id == st.session_state.user_id).first()
            user = db.query(User).filter(User.id == st.session_state.user_id).first()
            
            if not assessment:
                st.warning("Please complete fitness assessment first.")
            else:
                pdf_buffer = generate_pdf_report(user, assessment, workout_plan, diet_plan)
                st.download_button(
                    label="⬇️ Click here to Download PDF",
                    data=pdf_buffer,
                    file_name="Fitness_Report.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"Error generating PDF: {e}")
        finally:
            db.close()

