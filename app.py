import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime
from task_manager import TaskManager

# Page Configuration
st.set_page_config(
    page_title="TASKORA | Smart Productivity Platform",
    page_icon="🚀",
    layout="wide"
)

# Initialize Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "nav_target" not in st.session_state:
    st.session_state.nav_target = "🏠 Command Center"

# ----------------- SECURE LOGIN SCREEN -----------------
if not st.session_state.authenticated:
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
            html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
            .stApp { background: #080B12; color: #F8FAFC; }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🔐 TASKORA Login</h1>", unsafe_allow_html=True)
        with st.form("login_form"):
            email = st.text_input("Email Address", value="admin@taskora.com")
            password = st.text_input("Password", type="password", value="password123")
            submitted = st.form_submit_button("Access Workspace")
            
            if submitted:
                if email and password:
                    st.session_state.authenticated = True
                    st.session_state.user = email.split('@')[0].capitalize()
                    st.success("Welcome back, Productivity Pro!")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
    st.stop()

# ----------------- MAIN APP SUITE -----------------
manager = TaskManager()
is_dark = st.session_state.theme == "Dark"

# SaaS Color System & CSS Injection
bg_color = "#080B12" if is_dark else "#F8FAFC"
card_bg = "#111827" if is_dark else "#FFFFFF"
text_color = "#F8FAFC" if is_dark else "#0F172A"
sidebar_bg = "#05080F" if is_dark else "#E2E8F0"
sidebar_text = "#F8FAFC" if is_dark else "#0F172A"
btn_bg = "linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)" if is_dark else "linear-gradient(135deg, #4F46E5 0%, #312E81 100%)"

st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}
        .stApp {{ background: {bg_color}; color: {text_color}; }}
        
        [data-testid="stSidebar"] {{ background-color: {sidebar_bg}; border-right: 1px solid #1E293B; }}
        [data-testid="stSidebar"] span, [data-testid="stSidebar"] label, [data-testid="stSidebar"] div {{
            color: {sidebar_text} !important;
        }}
        
        .highlight-heading {{
            background: linear-gradient(90deg, #6366F1, #A855F7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }}
        
        .hero {{
            background: linear-gradient(90deg, rgba(8,11,18,.95), rgba(8,11,18,.45)), 
                        url('https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1600&q=80');
            height: 240px; border-radius: 20px; background-size: cover; background-position: center;
            padding: 35px; display: flex; align-items: center; margin-bottom: 25px;
            border: 1px solid rgba(255,255,255,.08); color: white;
        }}
        
        .hero-badge {{
            background: rgba(99,102,241,.3); padding: 6px 12px; border-radius: 15px; color: #A5B4FC; font-size: 12px;
        }}
        
        .task-card {{
            background: {card_bg}; border: 1px solid rgba(99,102,241,0.2);
            padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            margin-bottom: 15px; color: {text_color};
            transition: all 0.25s ease;
        }}
        .task-card:hover {{
            transform: translateY(-4px);
            border-color: #6366F1;
            box-shadow: 0 12px 30px rgba(99,102,241,.18);
        }}
        
        .tag {{
            display: inline-block; padding: 4px 10px; margin: 2px; border-radius: 12px;
            background: rgba(99,102,241,.15); color: #6366F1; font-size: 11px; font-weight: 600;
        }}

        .stButton>button {{
            background: {btn_bg}; color: #FFFFFF !important; border-radius: 10px; font-weight: 600; border: none;
            box-shadow: 0 4px 12px rgba(99,102,241,0.3); width: 100%;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(99,102,241,0.5);
        }}
    </style>
""", unsafe_allow_html=True)

# Top Bar Profile Widget & Notification Center
top_col1, top_col2, top_col3 = st.columns([5, 1.5, 1])
with top_col2:
    st.markdown("""
        <div style="background: rgba(30,41,59,0.5); padding: 6px 12px; border-radius: 12px; border: 1px solid #334155; display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.1rem;">👤</span>
            <div>
                <p style="margin:0; font-size: 0.85rem; font-weight: 600;">Admin</p>
                <p style="margin:0; font-size: 0.7rem; color: #22C55E;">● Online</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
with top_col3:
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

# Sidebar Navigation Suite with Index Routing
nav_options = [
    "🏠 Command Center",
    "➕ Add Task",
    "📋 Smart Tasks",
    "🗂️ Kanban Board",
    "🎯 Focus Mode",
    "📊 Analytics",
    "🤖 AI Assistant"
]

st.sidebar.markdown("<h2 style='text-align: center; color: #6366F1;'>🚀 TASKORA</h2>", unsafe_allow_html=True)

theme_choice = st.sidebar.radio("Theme Mode", ["🌙 Dark", "☀ Light"], index=0 if is_dark else 1)
if theme_choice.startswith("🌙") and not is_dark:
    st.session_state.theme = "Dark"
    st.rerun()
elif theme_choice.startswith("☀") and is_dark:
    st.session_state.theme = "Light"
    st.rerun()

st.sidebar.markdown("---")

default_index = nav_options.index(st.session_state.nav_target) if st.session_state.nav_target in nav_options else 0

choice = st.sidebar.radio(
    "Navigation Workspace", 
    nav_options,
    index=default_index
)

st.session_state.nav_target = choice

# Sidebar Settings & Help
st.sidebar.markdown("---")
st.sidebar.markdown("⚙️ **Settings**")
st.sidebar.markdown("❓ **Help & Docs**")

# ─────────────────────────────────────
# 🏠 COMMAND CENTER
# ─────────────────────────────────────
if choice == "🏠 Command Center":

    # Hero Section with embedded New Task CTA button
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown("""
            <div class="hero" style="margin-bottom: 0px;">
                <div class="hero-content">
                    <span class="hero-badge">✨ PRODUCTIVITY HUB</span>
                    <h1 style="font-size: 2.6rem; margin: 8px 0; color: white;">Turn plans into progress.</h1>
                    <p style="color: #CBD5E1; font-size: 0.95rem;">Organize tasks, prioritize what matters, and stay focused on your goals.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col_h2:
        st.write("")
        st.write("")
        st.write("")
        if st.button("➕ New Task", use_container_width=True):
            st.session_state.nav_target = "➕ Add Task"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Metrics Overview
    total, completed, pending, high_priority, score = manager.get_stats()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📋 Total Tasks", total)
    m2.metric("✅ Completed", completed)
    m3.metric("⏳ Pending", pending)
    m4.metric("🏆 Productivity Score", f"{score}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # Two-Column Layout: Continue Where You Left Off & Today's Focus
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 🔥 <span class='highlight-heading'>Continue Where You Left Off</span>", unsafe_allow_html=True)
        pending_tasks = [t for t in manager.tasks if t.status == "Pending"]
        if not pending_tasks:
            st.info("No pending tasks right now. Great job!")
        else:
            t = pending_tasks[0]
            prio_color = "red" if t.priority == "High" else "orange" if t.priority == "Medium" else "green"
            st.markdown(f"""
                <div class="task-card">
                    <span style="color: {prio_color}; font-weight: 700; font-size: 12px;">● {t.priority.upper()} PRIORITY</span>
                    <h3 style="margin: 8px 0;">{t.title}</h3>
                    <p style="color: #94A3B8; font-size: 13px;">💻 {t.category} &nbsp;|&nbsp; 📅 Due: {t.due_date}</p>
                    <div style="background: #1E293B; border-radius: 8px; height: 8px; width: 100%; margin: 15px 0;">
                        <div style="background: #6366F1; width: 80%; height: 8px; border-radius: 8px;"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Continue Task →", key="cont_btn"):
                st.session_state.nav_target = "📋 Smart Tasks"
                st.rerun()

    with col_right:
        st.markdown("### 🎯 <span class='highlight-heading'>Today's Focus</span>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="task-card">
                <p style="color: #A5B4FC; font-weight: 600; margin-bottom: 10px;">3 high-priority focus goals today</p>
                <div style="font-size: 14px; line-height: 1.8;">
                    ☐ Complete pending assignment<br>
                    ☐ Push build updates to GitHub<br>
                    ☑ Review product documentation
                </div>
                <hr style="border: 0; height: 1px; background: #334155; margin: 15px 0;">
                <p style="color: #22C55E; font-weight: 600; font-size: 13px; margin: 0;">67% completed today</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Upcoming Deadlines & Weekly Productivity Chart Layout
    d_col1, d_col2 = st.columns(2)

    with d_col1:
        st.markdown("### 📅 <span class='highlight-heading'>Upcoming Deadlines</span>", unsafe_allow_html=True)
        st.markdown("""
            <div class="task-card">
                <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <span>🔴 Python Project Build</span><span style="color: #F59E0B; font-weight: 600;">Tomorrow</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <span>🟠 Analytics Assignment</span><span style="color: #94A3B8;">09 Aug</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 8px 0;">
                    <span>🟢 GitHub README Docs</span><span style="color: #22C55E;">12 Aug</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with d_col2:
        st.markdown("### 📈 <span class='highlight-heading'>Weekly Productivity</span>", unsafe_allow_html=True)
        chart_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Completion': [40, 75, 60, 90, 85, 30, 50]
        })
        fig = px.line(chart_data, x='Day', y='Completion', markers=True, color_discrete_sequence=["#6366F1"])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=10, b=10),
            height=160,
            xaxis=dict(showgrid=False, color='#94A3B8'),
            yaxis=dict(showgrid=True, gridcolor='#1E293B', color='#94A3B8')
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Achievements & Streak Counter Layout
    a_col1, a_col2 = st.columns(2)

    with a_col1:
        st.markdown("### 🏆 <span class='highlight-heading'>Your Achievements</span>", unsafe_allow_html=True)
        st.markdown("""
            <div class="task-card" style="display: flex; gap: 20px; align-items: center;">
                <div style="font-size: 2.5rem;">🥇</div>
                <div>
                    <h4 style="margin: 0; color: #F8FAFC;">Fast Finisher</h4>
                    <p style="margin: 0; color: #94A3B8; font-size: 12px;">Completed 5 critical tasks this week.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with a_col2:
        st.markdown("### 🔥 <span class='highlight-heading'>Productivity Streak</span>", unsafe_allow_html=True)
        st.markdown("""
            <div class="task-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h2 style="margin: 0; color: #F59E0B;">🔥 4 DAY STREAK</h2>
                        <p style="margin: 0; color: #94A3B8; font-size: 12px;">Consistency drives excellence.</p>
                    </div>
                    <div style="text-align: right; font-size: 13px; font-weight: 600; color: #22C55E;">
                        Mon ✓ &nbsp; Tue ✓ &nbsp; Wed ✓ &nbsp; Thu ✓
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────
# ➕ ADD TASK
# ─────────────────────────────────────
elif choice == "➕ Add Task":
    st.markdown("<h3>➕ <span class='highlight-heading'>Create a New Task Record</span></h3><p>Turn your plans into actionable goals.</p>", unsafe_allow_html=True)
    
    with st.form("comprehensive_add_form", clear_on_submit=True):
        title = st.text_input("Task Title")
        col1, col2, col3 = st.columns(3)
        with col1:
            priority = st.selectbox("Priority Level", ["High", "Medium", "Low"])
        with col2:
            category = st.selectbox("Category", ["💻 Coding", "📚 Study", "🏠 Personal", "🏋 Fitness", "💼 Office"])
        with col3:
            due_date = st.date_input("Due Date", value=date.today())
            
        tags_input = st.text_input("Tags (comma separated)", value="#Python, #Urgent")
        notes = st.text_area("Detailed Notes & Specifications")
        est_time = st.slider("Estimated Time Allocation (Hours)", 1, 10, 3)
        
        submitted = st.form_submit_button("Commit Task to Database")
        if submitted:
            if title.strip():
                tags_list = [t.strip() for t in tags_input.split(",")]
                manager.add_task(title, priority, due_date, category, tags_list, notes, est_time)
                st.success("🎉 Task created successfully with full attributes assigned!")
            else:
                st.error("Task title is required.")

# ─────────────────────────────────────
# 📋 SMART TASKS
# ─────────────────────────────────────
elif choice == "📋 Smart Tasks":
    st.markdown("<h3>📋 <span class='highlight-heading'>Smart Tasks Repository</span></h3><p>Search, filter, sort, and manage your active objectives.</p>", unsafe_allow_html=True)
    
    # Filter Controls Bar
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    with f_col1:
        search_query = st.text_input("🔍 Search tasks...")
    with f_col2:
        status_filter = st.selectbox("Status", ["All", "Pending", "In Progress", "Done"])
    with f_col3:
        priority_filter = st.selectbox("Priority", ["All", "High", "Medium", "Low"])
    with f_col4:
        sort_by = st.selectbox("Sort By", ["Due Date", "Priority", "Title", "Created Time"])

    # Filtering Logic
    filtered = manager.tasks
    if search_query:
        filtered = [t for t in filtered if search_query.lower() in t.title.lower()]
    if status_filter != "All":
        filtered = [t for t in filtered if t.status == status_filter]
    if priority_filter != "All":
        filtered = [t for t in filtered if t.priority == priority_filter]

    # Sorting Logic
    if sort_by == "Priority":
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        filtered = sorted(filtered, key=lambda x: priority_order.get(x.priority, 2))
    elif sort_by == "Title":
        filtered = sorted(filtered, key=lambda x: x.title)
    elif sort_by == "Due Date":
        filtered = sorted(filtered, key=lambda x: x.due_date)

    st.markdown("---")

    if not filtered:
        st.info("No tasks matching your filter criteria.")
    else:
        for t in filtered:
            col_card, col_actions = st.columns([4, 1.2])
            
            prio_color = "red" if t.priority == "High" else "orange" if t.priority == "Medium" else "green"
            status_icon = "✅" if t.status == "Done" else "⏳"
            
            with col_card:
                st.markdown(f"""
                    <div class="task-card" style="padding: 15px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: {prio_color}; font-weight: 700; font-size: 11px;">● {t.priority.upper()}</span>
                            <span style="font-size: 11px; color: #94A3B8;">📅 {t.due_date} | 💻 {t.category}</span>
                        </div>
                        <h4 style="margin: 6px 0 4px 0;">{status_icon} {t.title}</h4>
                        <p style="color: #94A3B8; font-size: 12px; margin: 0;">{t.notes or 'No additional details specified.'}</p>
                    </div>
                """, unsafe_allow_html=True)
                
            with col_actions:
                st.write("")
                if t.status != "Done":
                    if st.button("✓ Done", key=f"smart_done_{t.id}"):
                        manager.update_task(t.id, "", "", "Done", "", "")
                        st.rerun()
                else:
                    if st.button("↺ Reopen", key=f"smart_open_{t.id}"):
                        manager.update_task(t.id, "", "", "Pending", "", "")
                        st.rerun()
                        
                if st.button("🗑️ Delete", key=f"smart_del_{t.id}"):
                    manager.delete_task(t.id)
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        # Export CSV Option
        df_export = pd.DataFrame([t.to_dict() for t in filtered])
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        st.download_button("📤 Export Filtered Tasks to CSV", data=csv_data, file_name="taskora_tasks.csv", mime="text/csv")

# ─────────────────────────────────────
# 🗂️ KANBAN BOARD
# ─────────────────────────────────────
elif choice == "🗂️ Kanban Board":
    st.markdown("### 🗂️ <span class='highlight-heading'>Agile Kanban Workflow</span>", unsafe_allow_html=True)
    k1, k2, k3 = st.columns(3)
    
    pending = [t for t in manager.tasks if t.status == "Pending"]
    doing = [t for t in manager.tasks if t.status == "In Progress"]
    done = [t for t in manager.tasks if t.status == "Done"]
    
    with k1:
        st.markdown("#### 📋 TODO")
        for t in pending:
            st.markdown(f"<div class='task-card'><b>{t.title}</b><br><small>{t.priority} Priority</small></div>", unsafe_allow_html=True)
            if st.button(f"Start #{t.id}", key=f"k_start_{t.id}"):
                manager.update_task(t.id, "", "", "In Progress", "", "")
                st.rerun()
    with k2:
        st.markdown("#### 🔄 IN PROGRESS")
        for t in doing:
            st.markdown(f"<div class='task-card'><b>{t.title}</b><br><small>In Execution</small></div>", unsafe_allow_html=True)
            if st.button(f"Complete #{t.id}", key=f"k_comp_{t.id}"):
                manager.update_task(t.id, "", "", "Done", "", "")
                st.rerun()
    with k3:
        st.markdown("#### ✅ COMPLETED")
        for t in done:
            st.markdown(f"<div class='task-card'><b>{t.title}</b><br><small>Finished</small></div>", unsafe_allow_html=True)

# ─────────────────────────────────────
# 🎯 FOCUS MODE
# ─────────────────────────────────────
elif choice == "🎯 Focus Mode":
    st.markdown("### 🎯 <span class='highlight-heading'>Deep Work Focus Studio</span>", unsafe_allow_html=True)
    
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        st.markdown("""
            <div class="task-card" style="text-align: center; padding: 40px;">
                <h2>⏱ POMODORO TIMER</h2>
                <h1 style="font-size: 5rem; color: #6366F1; margin: 20px 0;">25:00</h1>
                <p style="color: #94A3B8;">Stay distraction-free. Focus session in progress.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("▶ Start Focus Session"):
            st.success("Focus timer initiated! Notifications silenced.")
    with col_f2:
        st.markdown("### 🏆 Achievements Unlocked")
        st.markdown("- 🥇 First Task Completed")
        st.markdown("- 🔥 4 Day Productivity Streak")
        st.markdown("- ⚡ Focus Master (Level 7)")

# ─────────────────────────────────────
# 📊 ANALYTICS
# ─────────────────────────────────────
elif choice == "📊 Analytics":
    st.markdown("### 📊 <span class='highlight-heading'>Productivity Analytics Engine</span>", unsafe_allow_html=True)
    total, completed, pending, high_priority, score = manager.get_stats()
    
    if total > 0:
        df = pd.DataFrame([t.to_dict() for t in manager.tasks])
        ac1, ac2 = st.columns(2)
        with ac1:
            fig_pie = px.pie(df, names="status", title="Task Completion Ratio", hole=0.5, color_discrete_sequence=["#6366F1", "#22C55E"])
            st.plotly_chart(fig_pie, use_container_width=True)
        with ac2:
            fig_bar = px.bar(df, x="priority", title="Priority Volume Breakdown", color="priority", color_discrete_sequence=["#EF4444", "#F59E0B", "#22C55E"])
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Insufficient task data for rendering analytical graphs.")

# ─────────────────────────────────────
# 🤖 AI ASSISTANT
# ─────────────────────────────────────
elif choice == "🤖 AI Assistant":
    st.markdown("### 🤖 <span class='highlight-heading'>TASKORA Copilot AI</span>", unsafe_allow_html=True)
    goal = st.text_input("What goal would you like AI to break down into action items?", value="Prepare Fullstack React & Python project")
    
    if st.button("✨ Ask TASKORA AI"):
        st.markdown("---")
        st.markdown(f"#### 🧠 Structured Plan for: *{goal}*")
        st.markdown("1. **Architecture & Schema Design** — *Estimated: 45 min*")
        st.markdown("2. **Core Backend Logic & API Routes** — *Estimated: 90 min*")
        st.markdown("3. **Streamlit Interactive UI Layout** — *Estimated: 60 min*")
        st.markdown("4. **Integration Testing & Deployment** — *Estimated: 30 min*")
        st.success("Plan generated successfully! You can add these directly to your tasks.")

# Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.markdown(f"<p style='text-align: center; font-size: 0.8rem;'>TASKORA Suite v6.0 • Enterprise Edition</p>", unsafe_allow_html=True)