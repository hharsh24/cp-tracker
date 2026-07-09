import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Configuration
API_URL = "http://localhost:8000"
st.set_page_config(page_title="CP Mastery Tracker", page_icon="🏆", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
<style>
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stTextInput>div>div>input {
        background-color: #1e293b;
        color: white;
    }
    .stSelectbox>div>div>div {
        background-color: #1e293b;
        color: white;
    }
    .stTextArea>div>div>textarea {
        background-color: #1e293b;
        color: white;
    }
    .stButton>button {
        background-color: #6366f1;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #4f46e5;
        border-color: #4f46e5;
        color: white;
    }
    .card {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .tag {
        background-color: rgba(99, 102, 241, 0.2);
        color: #818cf8;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .virtual-tag {
        background-color: rgba(139, 92, 246, 0.2);
        color: #c4b5fd;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'token' not in st.session_state:
    st.session_state.token = None
if 'username' not in st.session_state:
    st.session_state.username = None

# Helper Functions
def get_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else {}

# --- AUTHENTICATION ---
if not st.session_state.token:
    st.title("🏆 CP Mastery Tracker")
    st.write("Welcome! Please log in or sign up to continue.")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            if submit:
                res = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
                if res.status_code == 200:
                    st.session_state.token = res.json().get("access_token")
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid username or password")
                    
    with tab2:
        with st.form("signup_form", clear_on_submit=True):
            new_username = st.text_input("Choose a Username")
            new_password = st.text_input("Choose a Password", type="password")
            submit_signup = st.form_submit_button("Sign Up")
            if submit_signup:
                res = requests.post(f"{API_URL}/signup", json={"username": new_username, "password": new_password})
                if res.status_code == 200:
                    st.toast("🎉 Account created successfully! You can now log in.")
                else:
                    try:
                        err_msg = res.json().get("detail", "Error creating account")
                    except Exception:
                        err_msg = f"Server Error {res.status_code}: {res.text}"
                    st.error(err_msg)
                    
    st.stop() # Stop execution if not logged in

# --- MAIN APP ---
st.sidebar.title(f"👋 Hi, {st.session_state.username}")
menu = st.sidebar.radio("Navigation", ["Dashboard", "Log Problem", "Review Vault", "Code Templates"])

if st.sidebar.button("Logout"):
    st.session_state.token = None
    st.session_state.username = None
    st.rerun()

# --- DASHBOARD ---
if menu == "Dashboard":
    st.title("📊 Dashboard Overview")
    
    res = requests.get(f"{API_URL}/logs/", headers=get_headers())
    if res.status_code == 200:
        logs = res.json()
        if not logs:
            st.info("No problems logged yet. Go to 'Log Problem' to get started!")
        else:
            col1, col2, col3 = st.columns(3)
            cf_count = sum(1 for log in logs if log.get('platform') == 'Codeforces')
            lc_count = sum(1 for log in logs if log.get('platform') == 'LeetCode')
            with col1:
                st.markdown(f"<div class='card'><h3>Total Logs</h3><h1 style='color:#6366f1'>{len(logs)}</h1></div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='card'><h3>Codeforces</h3><h1 style='color:#3b82f6'>{cf_count}</h1></div>", unsafe_allow_html=True) 
            with col3:
                st.markdown(f"<div class='card'><h3>LeetCode</h3><h1 style='color:#f59e0b'>{lc_count}</h1></div>", unsafe_allow_html=True)
            
            st.subheader("Mistakes by Pattern")
            df = pd.DataFrame(logs)
            pattern_counts = df['pattern'].value_counts().reset_index()
            pattern_counts.columns = ['Pattern', 'Count']
            
            fig = px.pie(pattern_counts, values='Count', names='Pattern', hole=0.6,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#f8fafc')
            st.plotly_chart(fig, use_container_width=True)
            
# --- LOG PROBLEM ---
elif menu == "Log Problem":
    st.title("📝 Log a Problem")
    
    with st.form("log_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            platform = st.selectbox("Platform", ["Codeforces", "LeetCode", "AtCoder", "Other"])
            contest_name = st.text_input("Contest Name (Optional)", placeholder="e.g. CF Round 950")
            is_virtual = st.checkbox("This was a Virtual Contest")
        with col2:
            pattern = st.selectbox("Core Pattern", ["Dynamic Programming", "Graphs / DFS / BFS", "Two Pointers", "Binary Search", "Greedy", "Math / Number Theory", "Trees", "Other"])
            contest_date = st.date_input("Contest Date (Optional)")
            
        link = st.text_input("Question Link / Name")
        concept = st.text_area("Core Concept / Solution Idea", placeholder="Main trick to solve without full code...")
        mistake = st.text_area("Mistake Made", placeholder="What did you do wrong?")
        learning = st.text_area("Key Learning", placeholder="What to remember for next time?")
        
        submitted = st.form_submit_button("Save Log")
        if submitted:
            data = {
                "platform": platform,
                "pattern": pattern,
                "contest_name": contest_name if contest_name else None,
                "contest_date": str(contest_date) if contest_date else None,
                "is_virtual": is_virtual,
                "link": link,
                "concept": concept,
                "mistake": mistake,
                "learning": learning
            }
            res = requests.post(f"{API_URL}/logs/", json=data, headers=get_headers())
            if res.status_code == 200:
                st.toast("✅ Log saved successfully!")
            else:
                st.error("Error saving log")

# --- REVIEW VAULT ---
elif menu == "Review Vault":
    st.title("📚 Review Vault")
    
    res = requests.get(f"{API_URL}/logs/", headers=get_headers())
    if res.status_code == 200:
        logs = res.json()
        
        # Filters
        patterns = ["All"] + list(set(log['pattern'] for log in logs))
        filter_pattern = st.selectbox("Filter by Pattern", patterns)
        
        filtered_logs = logs if filter_pattern == "All" else [log for log in logs if log['pattern'] == filter_pattern]
        
        if not filtered_logs:
            st.info("No logs match your filter.")
            
        for log in filtered_logs:
            virtual_badge = "<span class='virtual-tag'>Virtual</span>" if log.get('is_virtual') else ""
            contest_info = f" | 🗓️ {log.get('contest_name')} ({log.get('contest_date')}) {virtual_badge}" if log.get('contest_name') else ""
            
            st.markdown(f"""
            <div class='card'>
                <div style='display: flex; justify-content: space-between; margin-bottom: 15px;'>
                    <div>
                        <strong><span style='color: #6366f1'>{log['platform']}</span></strong>
                        <a href='{log['link']}' target='_blank' style='color: #f8fafc; margin-left: 10px; text-decoration: none;'>{log['link'][:50]}...</a>
                        <br>
                        <small style='color: #94a3b8;'>{contest_info}</small>
                    </div>
                    <div>
                        <span class='tag'>{log['pattern']}</span>
                    </div>
                </div>
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px;'>
                    <div>
                        <h5 style='color: #94a3b8;'>Core Concept</h5>
                        <p>{log['concept']}</p>
                    </div>
                    <div>
                        <h5 style='color: #f43f5e;'>Mistake Made</h5>
                        <p>{log['mistake']}</p>
                    </div>
                </div>
                <div style='background-color: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.2); padding: 15px; border-radius: 8px; margin-top: 15px;'>
                    <h5 style='color: #34d399; margin:0 0 5px 0;'>Key Learning</h5>
                    <p style='margin:0;'>{log['learning']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Delete", key=f"del_{log['id']}"):
                requests.delete(f"{API_URL}/logs/{log['id']}", headers=get_headers())
                st.rerun()

# --- CODE TEMPLATES ---
elif menu == "Code Templates":
    st.title("🧩 Code Templates")
    st.write("Save your reusable snippets (e.g., Segment Tree, Fast I/O, DSU) here.")
    
    with st.expander("➕ Add New Template", expanded=False):
        with st.form("template_form", clear_on_submit=True):
            t_title = st.text_input("Title (e.g., Fenwick Tree)")
            t_lang = st.selectbox("Language", ["cpp", "python", "java"])
            t_desc = st.text_input("Short Description")
            t_code = st.text_area("Code", height=200)
            
            if st.form_submit_button("Save Template"):
                data = {"title": t_title, "language": t_lang, "description": t_desc, "code": t_code}
                res = requests.post(f"{API_URL}/templates/", json=data, headers=get_headers())
                if res.status_code == 200:
                    st.toast("✅ Template saved!")
                    st.rerun()
                else:
                    st.error("Error saving template")
                    
    res = requests.get(f"{API_URL}/templates/", headers=get_headers())
    if res.status_code == 200:
        templates = res.json()
        if not templates:
            st.info("No templates saved yet.")
        for temp in templates:
            with st.container():
                st.markdown(f"<div class='card'>", unsafe_allow_html=True)
                col1, col2 = st.columns([0.9, 0.1])
                with col1:
                    st.subheader(temp['title'])
                    st.caption(f"Language: `{temp['language']}` | {temp['description']}")
                with col2:
                    if st.button("🗑️", key=f"delt_{temp['id']}"):
                        requests.delete(f"{API_URL}/templates/{temp['id']}", headers=get_headers())
                        st.rerun()
                st.code(temp['code'], language=temp['language'])
                st.markdown("</div>", unsafe_allow_html=True)
