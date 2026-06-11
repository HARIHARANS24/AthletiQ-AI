import streamlit as st
import plotly.express as px
from utils.helpers import render_sidebar_nav
from services.analytics_service import get_user_progress_data
from services.gemini_service import generate_weekly_insights
import json

if "user_id" not in st.session_state or st.session_state.user_id is None:
    st.warning("Please log in to view this page.")
    st.stop()

render_sidebar_nav()

st.title("📉 Analytics & AI Insights")

df = get_user_progress_data(st.session_state.user_id)

if df.empty:
    st.info("Not enough data to generate analytics. Please log your progress in the Progress Tracker.")
    st.stop()

# Charts
tab1, tab2, tab3 = st.tabs(["Trends", "Consistency", "AI Insights"])

with tab1:
    st.subheader("Weight Trend")
    fig_weight = px.line(df, x="Date", y="Weight", markers=True, title="Weight Over Time")
    st.plotly_chart(fig_weight, use_container_width=True)
    
    st.subheader("Daily Calories")
    fig_cal = px.bar(df, x="Date", y="Calories", title="Calorie Intake Over Time", color="Calories", color_continuous_scale="Viridis")
    st.plotly_chart(fig_cal, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Water Intake")
        fig_water = px.line(df, x="Date", y="Water", markers=True, title="Daily Water (L)")
        st.plotly_chart(fig_water, use_container_width=True)
    with col2:
        st.subheader("Sleep Patterns")
        fig_sleep = px.bar(df, x="Date", y="Sleep", title="Sleep Duration (Hrs)")
        st.plotly_chart(fig_sleep, use_container_width=True)
        
    st.subheader("Workout Consistency")
    completed = df[df["Workout Completed"] == True].shape[0]
    total = df.shape[0]
    percentage = (completed / total) * 100 if total > 0 else 0
    st.metric("Workouts Completed (Recorded Days)", f"{completed} / {total} ({percentage:.1f}%)")

with tab3:
    st.subheader("AI Weekly Insights")
    st.write("Get AI-powered analysis of your recent progress data.")
    
    if st.button("Generate Insight Report"):
        with st.spinner("AI is analyzing your data..."):
            try:
                recent_data = df.tail(7).to_json(orient="records", date_format="iso")
                insights = generate_weekly_insights(recent_data)
                
                st.success("Report Generated")
                st.markdown(f"**Summary:** {insights.get('Summary', '')}")
                st.metric("Adherence Score", insights.get('AdherenceScore', 'N/A'))
                
                col3, col4 = st.columns(2)
                with col3:
                    st.markdown("### Positives 🌟")
                    for p in insights.get('Positives', []):
                        st.markdown(f"- {p}")
                with col4:
                    st.markdown("### Needs Improvement ⚠️")
                    for a in insights.get('AreasForImprovement', []):
                        st.markdown(f"- {a}")
                        
                st.markdown("### Coach's Suggestions 💡")
                for s in insights.get('Suggestions', []):
                    st.info(s)
            except Exception as e:
                st.error(f"Failed to generate insights: {e}")
