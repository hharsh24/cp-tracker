# 🏆 CP Mastery Tracker

A modern, full-stack application designed specifically for Competitive Programmers to track their progress, analyze mistakes, and manage a personal code vault for Codeforces, LeetCode, and AtCoder.

## ✨ Features

- **Multi-User Authentication**: Securely sign up and log in. Your data is 100% private to your account.
- **Log Problems**: Keep track of the problems you've solved during real or virtual contests. Note down the core concept, the mistakes you made, and key learnings.
- **Smart Dashboard**: Visualize your progress with dynamic metrics and interactive charts analyzing your mistakes by algorithmic pattern (e.g., DP, Graphs, Binary Search).
- **Review Vault**: Filter and review past problems by pattern so you never make the same mistake twice.
- **Code Templates**: A dedicated vault for your reusable snippets (Segment Trees, DSU, Fast I/O) with syntax highlighting. Copy them instantly during a contest!

## 🚀 Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) - Lightning fast Python backend.
- **Frontend**: [Streamlit](https://streamlit.io/) - Beautiful, responsive UI.
- **Database**: SQLite (via SQLAlchemy) - Lightweight, zero-config local storage.
- **Security**: bcrypt & JWT (JSON Web Tokens) for safe authentication.

## 🛠️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/hharsh24/cp-tracker.git
   cd cp-tracker
   ```

2. **Install Dependencies**
   It's recommended to use a virtual environment. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Backend Server (FastAPI)**
   Open a terminal in the project root directory and run:
   ```bash
   python -m uvicorn backend.main:app --port 8000
   ```

4. **Start the Frontend App (Streamlit)**
   Open a **second** terminal in the project root directory and run:
   ```bash
   python -m streamlit run frontend/app.py --server.port 8501
   ```

5. **Open the App**
   Navigate to [http://localhost:8501](http://localhost:8501) in your browser. Create an account and start tracking your CP mastery!

---

*Made with ❤️ for the Competitive Programming Community.*
