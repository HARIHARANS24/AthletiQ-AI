# 🏋️‍♂️ AI-Powered Personalized Workout & Diet Planner 🥗

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Google%20Gemini%20API-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLAlchemy" />
</div>

<br />

A comprehensive, cutting-edge fitness application that leverages the power of **Google Gemini API** to provide highly personalized workout routines and diet plans. Built with a sleek user interface using **Streamlit** and robust backend data management via **SQLAlchemy**, this application serves as your personal, AI-driven fitness coach and nutritionist.

---

## 📑 Table of Contents
- [✨ Key Features](#-key-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📂 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation & Setup](#installation--setup)
- [💻 Usage](#-usage)
- [🔮 Future Enhancements](#-future-enhancements)

---

## ✨ Key Features

- **🔐 Secure User Authentication:** Robust signup and login functionality using `bcrypt` for secure password hashing.
- **📝 Comprehensive Fitness Assessment:** Users can input detailed physical metrics, fitness goals, dietary preferences, and medical conditions to establish a baseline.
- **🤖 AI-Generated Workout & Diet Plans:** Utilizes Google's advanced Gemini AI to generate custom-tailored, dynamic workout and meal plans based on individual assessment data.
- **💬 AI Fitness Chatbot Coach:** An interactive virtual coach that answers health queries, provides motivation, and offers real-time fitness advice using Generative AI.
- **📈 Progress Tracking & Analytics:** Visual dashboards featuring interactive charts (powered by `Plotly` and `Pandas`) to monitor weight changes, workout consistency, and goal progression.
- **📄 PDF Report Generation:** Export personalized workout plans, diet charts, and progress summaries into professional PDF reports using `ReportLab`.
- **👤 Profile Management:** Easy-to-use interface for users to update their health metrics and preferences over time.

---

## 🛠️ Tech Stack

| Category | Technologies / Libraries Used |
| :--- | :--- |
| **Frontend Framework** | [Streamlit](https://streamlit.io/) (v1.36.0) |
| **Backend & Logic** | Python 3.x |
| **AI / LLM Engine** | [Google Generative AI](https://aistudio.google.com/) (Gemini API) |
| **Database & ORM** | SQLite, [SQLAlchemy](https://www.sqlalchemy.org/) (v2.0.30) |
| **Data Visualization** | Plotly (v5.22.0), Pandas (v2.2.2) |
| **PDF Generation** | ReportLab (v4.2.2) |
| **Security** | bcrypt (v4.1.3), python-dotenv |

---

## 📂 Project Structure

```text
├── app.py                  # Main entry point for the Streamlit application
├── requirements.txt        # Python dependencies required for the project
├── .env.example            # Example environment variables file
├── Dockerfile              # Docker configuration for containerized deployment
├── database/               # Database setup and SQLAlchemy models
│   ├── db.py               # Database connection configuration
│   └── models.py           # Database schema and ORM models
├── pages/                  # Streamlit application pages (UI components)
│   ├── analytics.py        # Progress and analytics dashboard
│   ├── assessment.py       # Fitness assessment forms
│   ├── chatbot.py          # AI Coach chat interface
│   ├── dashboard.py        # Main user dashboard overview
│   ├── diet.py             # Diet plan generation and display
│   ├── profile.py          # User profile management
│   ├── progress.py         # Daily/Weekly progress logging
│   └── workout.py          # Workout plan generation and tracking
├── services/               # Core business logic and API integrations
│   ├── analytics_service.py # Logic for data processing and charts
│   ├── auth_service.py      # Authentication and user management
│   ├── diet_service.py      # Diet plan specific logic
│   ├── gemini_service.py    # Integration with Google Gemini API
│   └── workout_service.py   # Workout plan specific logic
├── utils/                  # Utility functions and helpers
└── reports/                # Directory for generated PDF reports
```

---

## 🚀 Getting Started

Follow these instructions to set up the project locally on your machine.

### Prerequisites
- **Python 3.8+** installed on your system.
- A **Google Gemini API Key**. You can obtain one from [Google AI Studio](https://aistudio.google.com/).
- Git (optional, for cloning the repository).

### Installation & Setup

**1. Clone the repository**
```bash
git clone <your-repository-url>
cd "AI-Powered Personalized Workout & Diet Planner"
```

**2. Create a virtual environment**
It is highly recommended to use a virtual environment to manage dependencies.
```bash
python -m venv venv
```

**3. Activate the virtual environment**
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Linux/Mac:**
  ```bash
  source venv/bin/activate
  ```

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

**5. Configure Environment Variables**
Copy the `.env.example` file to create a new `.env` file in the root directory.
```bash
cp .env.example .env  # On Linux/Mac
copy .env.example .env # On Windows
```
Open `.env` and add your Gemini API Key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

**6. Initialize Database and Run the Application**
The database (`fitness_app.db`) will be automatically initialized via SQLAlchemy upon the first run.
```bash
streamlit run app.py
```

The application should now be running locally at `http://localhost:8501`.

---

## 💻 Usage

1. **Sign Up / Log In**: Start by creating a new account. Your credentials will be securely hashed.
2. **Complete Assessment**: Navigate to the Assessment page to input your current weight, height, dietary preferences, injuries, and specific fitness goals.
3. **Generate Plans**: Visit the Workout and Diet pages. The app will use the Gemini AI to analyze your assessment and generate a customized routine.
4. **Track Progress**: Log your daily macros, workout completion, and weight in the Progress section. Check the Analytics tab for interactive visualizations of your journey.
5. **Consult the AI Coach**: Head to the Chatbot page whenever you need motivation, recipe alternatives, or exercise form tips.
6. **Download Reports**: Export your data and plans as a PDF for offline viewing or printing.

---

## 🔮 Future Enhancements
- **Wearable Integration**: Sync with Apple Health, Google Fit, or Fitbit APIs to automatically pull daily activity data.
- **Social Features**: Add community challenges, leaderboards, and the ability to share progress with friends.
- **Advanced Computer Vision**: Allow users to upload videos of their exercises for AI-based form correction.
- **Multi-language Support**: Provide the UI and AI-generated plans in multiple languages.

---
