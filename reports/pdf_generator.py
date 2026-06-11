import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO

def generate_pdf_report(user_data, assessment_data, workout_plan, diet_plan) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = styles['Heading1']
    title_style.alignment = 1 # Center
    
    heading_style = styles['Heading2']
    normal_style = styles['Normal']
    
    story = []
    
    # Title
    story.append(Paragraph("Personalized Fitness & Diet Report", title_style))
    story.append(Spacer(1, 12))
    
    # User Profile
    story.append(Paragraph("User Profile", heading_style))
    profile_data = [
        ["Name", user_data.full_name],
        ["Age", str(user_data.age)],
        ["Gender", user_data.gender],
        ["Height", f"{user_data.height} cm"],
        ["Weight", f"{user_data.weight} kg"],
        ["Goal", user_data.fitness_goal or assessment_data.target_weight]
    ]
    t_profile = Table(profile_data, colWidths=[150, 300])
    t_profile.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
    ]))
    story.append(t_profile)
    story.append(Spacer(1, 12))
    
    # Workout Plan
    if workout_plan:
        story.append(Paragraph("Weekly Workout Plan", heading_style))
        for day, details in workout_plan.items():
            story.append(Paragraph(f"<b>{day} - {details.get('WorkoutType', 'Rest')}</b>", normal_style))
            if details.get('Warmup'):
                story.append(Paragraph(f"Warmup: {details['Warmup']}", normal_style))
            
            exercises = details.get('Exercises', [])
            if exercises:
                ex_data = [["Exercise", "Sets", "Reps", "Rest"]]
                for ex in exercises:
                    ex_data.append([ex.get('Exercise', ''), str(ex.get('Sets', '')), str(ex.get('Reps', '')), str(ex.get('Rest', ''))])
                
                t_ex = Table(ex_data, colWidths=[200, 50, 50, 100])
                t_ex.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F8BF9")),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
                ]))
                story.append(t_ex)
                
            if details.get('Cooldown'):
                story.append(Paragraph(f"Cooldown: {details['Cooldown']}", normal_style))
            story.append(Spacer(1, 8))

    # Diet Plan
    if diet_plan:
        story.append(Spacer(1, 12))
        story.append(Paragraph("Daily Diet Plan", heading_style))
        macros = diet_plan.get('DailyMacros', {})
        story.append(Paragraph(f"Target Calories: {diet_plan.get('TargetCalories', '')} kcal", normal_style))
        story.append(Paragraph(f"Macros -> Protein: {macros.get('Protein', '')} | Carbs: {macros.get('Carbs', '')} | Fats: {macros.get('Fats', '')}", normal_style))
        story.append(Spacer(1, 8))
        
        meals = diet_plan.get('Meals', {})
        for meal, m_details in meals.items():
            story.append(Paragraph(f"<b>{meal} ({m_details.get('Calories', '')} kcal)</b>", normal_style))
            items = ", ".join(m_details.get('Items', []))
            story.append(Paragraph(f"Items: {items}", normal_style))
            story.append(Paragraph(f"Protein: {m_details.get('Protein', '')} | Carbs: {m_details.get('Carbs', '')} | Fats: {m_details.get('Fats', '')}", normal_style))
            story.append(Spacer(1, 6))

    doc.build(story)
    buffer.seek(0)
    return buffer
