from database.db import SessionLocal
from database.models import ProgressLog, User, FitnessAssessment
import pandas as pd

def get_user_progress_data(user_id: int):
    db = SessionLocal()
    try:
        logs = db.query(ProgressLog).filter(ProgressLog.user_id == user_id).order_by(ProgressLog.date).all()
        if not logs:
            return pd.DataFrame()
            
        data = []
        for log in logs:
            data.append({
                "Date": log.date,
                "Weight": log.weight,
                "Calories": log.calories_consumed,
                "Water": log.water_intake,
                "Steps": log.steps,
                "Sleep": log.sleep_hours,
                "Workout Completed": log.workout_completed
            })
        return pd.DataFrame(data)
    finally:
        db.close()
        
def get_dashboard_metrics(user_id: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        latest_log = db.query(ProgressLog).filter(ProgressLog.user_id == user_id).order_by(ProgressLog.date.desc()).first()
        
        assessment = db.query(FitnessAssessment).filter(FitnessAssessment.user_id == user_id).first()
        
        metrics = {
            "current_weight": latest_log.weight if latest_log and latest_log.weight else (user.weight if user else 0),
            "target_weight": assessment.target_weight if assessment and assessment.target_weight else None,
            "latest_calories": latest_log.calories_consumed if latest_log else 0,
            "latest_water": latest_log.water_intake if latest_log else 0,
            "latest_sleep": latest_log.sleep_hours if latest_log else 0,
        }
        return metrics
    finally:
        db.close()
