import streamlit as st
from utils.helpers import render_sidebar_nav
from database.db import SessionLocal
from database.models import ChatHistory
from services.gemini_service import fitness_chat

if "user_id" not in st.session_state or st.session_state.user_id is None:
    st.warning("Please log in to view this page.")
    st.stop()

render_sidebar_nav()

st.title("🤖 AI Fitness Coach")
st.write("Ask me anything about fitness, nutrition, or your workout plan!")

db = SessionLocal()
try:
    # Initialize chat history in session state if not present
    if "messages" not in st.session_state:
        # Load from DB
        history = db.query(ChatHistory).filter(ChatHistory.user_id == st.session_state.user_id).order_by(ChatHistory.timestamp).all()
        st.session_state.messages = [{"role": msg.role, "content": msg.message} for msg in history]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What is your fitness question?"):
        # Display user message
        st.chat_message("user").markdown(prompt)
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Save user message to DB
        new_user_msg = ChatHistory(user_id=st.session_state.user_id, role="user", message=prompt)
        db.add(new_user_msg)
        db.commit()

        # Get AI response
        with st.chat_message("model"):
            message_placeholder = st.empty()
            with st.spinner("Thinking..."):
                try:
                    # Pass the DB objects to Gemini service to maintain context
                    db_history = db.query(ChatHistory).filter(ChatHistory.user_id == st.session_state.user_id).order_by(ChatHistory.timestamp).all()
                    response_text = fitness_chat(st.session_state.user_id, prompt, db_history[:-1]) # exclude the message just added
                    message_placeholder.markdown(response_text)
                    
                    st.session_state.messages.append({"role": "model", "content": response_text})
                    
                    # Save AI response to DB
                    new_ai_msg = ChatHistory(user_id=st.session_state.user_id, role="model", message=response_text)
                    db.add(new_ai_msg)
                    db.commit()
                except Exception as e:
                    st.error(f"Error communicating with AI Coach: {e}")
finally:
    db.close()
