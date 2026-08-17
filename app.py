"""
FitTrack - Personal Fitness Tracker
A mobile-first Streamlit app for tracking the 4-week workout plan.
iPhone-responsive design with native mobile fitness tracker behavior.
"""

import json
import os
from datetime import datetime, date, timedelta
import streamlit as st
from db import get_db, WorkoutDatabase

# ============================================================
# CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="FitTrack",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CSS - iPhone Responsive Mobile UI
# ============================================================
MOBILE_CSS = """
<style>
    /* Global mobile-first styles */
    * {
        box-sizing: border-box;
        -webkit-tap-highlight-color: transparent;
    }

    .stApp {
        background: #0f1117;
        color: #e8eaf0;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, sans-serif;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, header {
        visibility: hidden;
        height: 0;
    }

    .block-container {
        padding: 0.5rem 0.8rem 2rem 0.8rem;
        max-width: 480px;
        margin: 0 auto;
    }

    /* ===== Header ===== */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.8rem 0.2rem;
        margin-bottom: 0.5rem;
    }
    .app-title {
        font-size: 1.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    .app-date {
        font-size: 0.75rem;
        color: #8a8f9c;
        font-weight: 500;
    }

    /* ===== Week Selector ===== */
    .week-selector {
        display: flex;
        gap: 0.4rem;
        overflow-x: auto;
        padding: 0.3rem 0 0.8rem 0;
        scrollbar-width: none;
    }
    .week-selector::-webkit-scrollbar {
        display: none;
    }
    .week-chip {
        flex: 1;
        min-width: 70px;
        text-align: center;
        padding: 0.55rem 0.4rem;
        border-radius: 14px;
        background: #1a1d27;
        border: 1.5px solid #2a2e3a;
        font-size: 0.75rem;
        font-weight: 600;
        color: #8a8f9c;
        cursor: pointer;
        transition: all 0.2s ease;
        white-space: nowrap;
    }
    .week-chip.active {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-color: transparent;
        color: #0f1117;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
    }

    /* ===== Cardio Banner ===== */
    .cardio-banner {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        background: linear-gradient(135deg, #1a1d27 0%, #232838 100%);
        border: 1.5px solid #2a2e3a;
        border-radius: 16px;
        padding: 0.8rem 1rem;
        margin-bottom: 1rem;
    }
    .cardio-icon {
        font-size: 1.5rem;
    }
    .cardio-text {
        font-size: 0.85rem;
        font-weight: 600;
        color: #e8eaf0;
    }
    .cardio-sub {
        font-size: 0.7rem;
        color: #8a8f9c;
    }

    /* ===== Day Cards ===== */
    .day-card {
        background: #1a1d27;
        border: 1.5px solid #2a2e3a;
        border-radius: 16px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.6rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .day-card:hover {
        border-color: #4facfe;
        transform: translateY(-1px);
    }
    .day-card.today {
        border-color: #4facfe;
        background: linear-gradient(135deg, #1a1d27 0%, #1e2433 100%);
        box-shadow: 0 4px 20px rgba(79, 172, 254, 0.15);
    }
    .day-card.rest {
        opacity: 0.6;
    }
    .day-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.4rem;
    }
    .day-name {
        font-size: 0.95rem;
        font-weight: 700;
        color: #e8eaf0;
    }
    .day-badge {
        font-size: 0.65rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        background: #2a2e3a;
        color: #8a8f9c;
    }
    .day-badge.today {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: #0f1117;
    }
    .day-badge.done {
        background: #1e8e5a;
        color: #fff;
    }
    .day-exercises {
        font-size: 0.75rem;
        color: #8a8f9c;
        line-height: 1.5;
    }

    /* ===== Exercise Cards ===== */
    .exercise-card {
        background: #1a1d27;
        border: 1.5px solid #2a2e3a;
        border-radius: 14px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        transition: all 0.2s ease;
    }
    .exercise-card.completed {
        border-color: #1e8e5a;
        background: #16211c;
    }
    .exercise-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }
    .exercise-name {
        font-size: 0.9rem;
        font-weight: 700;
        color: #e8eaf0;
    }
    .exercise-meta {
        font-size: 0.7rem;
        color: #8a8f9c;
        font-weight: 500;
    }
    .exercise-check {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        border: 2px solid #3a3f4d;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.7rem;
        color: transparent;
        transition: all 0.2s ease;
    }
    .exercise-check.done {
        background: #1e8e5a;
        border-color: #1e8e5a;
        color: #fff;
    }

    /* ===== Progress Ring ===== */
    .progress-ring {
        text-align: center;
        padding: 1rem 0;
    }
    .progress-percent {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .progress-label {
        font-size: 0.75rem;
        color: #8a8f9c;
        margin-top: 0.2rem;
    }

    /* ===== Stats Grid ===== */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    .stat-card {
        background: #1a1d27;
        border: 1.5px solid #2a2e3a;
        border-radius: 14px;
        padding: 0.8rem 0.5rem;
        text-align: center;
    }
    .stat-value {
        font-size: 1.3rem;
        font-weight: 800;
        color: #e8eaf0;
    }
    .stat-label {
        font-size: 0.65rem;
        color: #8a8f9c;
        margin-top: 0.2rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* ===== Bottom Navigation ===== */
    /* Style the nav buttons as a fixed bottom bar */
    [data-testid="stHorizontalBlock"]:has(button) {
        position: fixed;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 480px;
        background: rgba(15, 17, 23, 0.95);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-top: 1px solid #2a2e3a;
        padding: 0.5rem 0.5rem 0.8rem 0.5rem;
        z-index: 1000;
        margin: 0;
        gap: 0.3rem;
    }
    /* Style nav buttons */
    [data-testid="stHorizontalBlock"]:has(button) .stButton > button {
        background: transparent;
        border: none;
        box-shadow: none;
        color: #8a8f9c;
        font-size: 0.65rem;
        font-weight: 600;
        padding: 0.4rem 0.2rem;
        border-radius: 12px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.15rem;
        line-height: 1.3;
        white-space: pre-line;
        min-height: 50px;
    }
    [data-testid="stHorizontalBlock"]:has(button) .stButton > button:hover {
        background: rgba(79, 172, 254, 0.1);
        color: #4facfe;
        transform: none;
        box-shadow: none;
    }
    [data-testid="stHorizontalBlock"]:has(button) .stButton > button:active {
        transform: scale(0.95);
    }
    /* Active nav button (primary type) */
    [data-testid="stHorizontalBlock"]:has(button) .stButton > button[kind="primary"] {
        background: rgba(79, 172, 254, 0.15);
        color: #4facfe;
        box-shadow: none;
    }
    [data-testid="stHorizontalBlock"]:has(button) .stButton > button[kind="primary"]:hover {
        background: rgba(79, 172, 254, 0.2);
        color: #4facfe;
    }
    /* Hide the emoji-only line break */
    [data-testid="stHorizontalBlock"]:has(button) .stButton p {
        margin: 0;
        text-align: center;
    }
    /* Ensure the nav buttons container is at the bottom */
    [data-testid="stHorizontalBlock"]:has(button) {
        margin-top: 1rem;
    }
    /* Add bottom padding to content so nav doesn't overlap */
    .block-container {
        padding-bottom: 5.5rem;
    }

    /* ===== Buttons ===== */
    .stButton > button {
        width: 100%;
        border-radius: 14px;
        border: none;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: #0f1117;
        font-weight: 700;
        font-size: 0.9rem;
        padding: 0.7rem 1rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.25);
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(79, 172, 254, 0.35);
    }
    .stButton > button:active {
        transform: scale(0.98);
    }

    /* ===== Inputs ===== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: #1a1d27;
        border: 1.5px solid #2a2e3a;
        border-radius: 12px;
        color: #e8eaf0;
        font-size: 0.9rem;
        padding: 0.6rem 0.8rem;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #4facfe;
        box-shadow: 0 0 0 2px rgba(79, 172, 254, 0.2);
    }

    /* ===== Selectbox ===== */
    .stSelectbox > div > div {
        background: #1a1d27;
        border: 1.5px solid #2a2e3a;
        border-radius: 12px;
        color: #e8eaf0;
    }

    /* ===== Tabs ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.3rem;
        background: #1a1d27;
        border-radius: 14px;
        padding: 0.3rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.4rem 0.8rem;
        font-size: 0.8rem;
        font-weight: 600;
        color: #8a8f9c;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: #0f1117 !important;
    }

    /* ===== Progress Bar ===== */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 10px;
    }
    .stProgress > div > div {
        background: #2a2e3a;
        border-radius: 10px;
    }

    /* ===== Expander ===== */
    .stExpander {
        background: #1a1d27;
        border: 1.5px solid #2a2e3a;
        border-radius: 14px;
    }
    .stExpander summary {
        font-weight: 600;
        color: #e8eaf0;
    }

    /* ===== Metrics ===== */
    [data-testid="stMetric"] {
        background: #1a1d27;
        border: 1.5px solid #2a2e3a;
        border-radius: 14px;
        padding: 0.8rem;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.4rem;
        font-weight: 800;
        color: #e8eaf0;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.7rem;
        color: #8a8f9c;
    }

    /* ===== Alerts ===== */
    .stAlert {
        border-radius: 14px;
        border: none;
    }

    /* ===== Divider ===== */
    hr {
        border-color: #2a2e3a;
        margin: 0.8rem 0;
    }

    /* ===== Scrollbar ===== */
    ::-webkit-scrollbar {
        width: 4px;
        height: 4px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: #2a2e3a;
        border-radius: 4px;
    }

    /* ===== Bottom padding for nav ===== */
    .block-container {
        padding-bottom: 5rem;
    }

    /* ===== Section Titles ===== */
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e8eaf0;
        margin: 1rem 0 0.6rem 0;
    }
    .section-sub {
        font-size: 0.75rem;
        color: #8a8f9c;
        margin-bottom: 0.8rem;
    }

    /* ===== Empty State ===== */
    .empty-state {
        text-align: center;
        padding: 2.5rem 1rem;
        color: #8a8f9c;
    }
    .empty-icon {
        font-size: 3rem;
        margin-bottom: 0.8rem;
    }
    .empty-text {
        font-size: 0.85rem;
        line-height: 1.6;
    }

    /* ===== History Card ===== */
    .history-card {
        background: #1a1d27;
        border: 1.5px solid #2a2e3a;
        border-radius: 14px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
    }
    .history-date {
        font-size: 0.8rem;
        font-weight: 700;
        color: #e8eaf0;
    }
    .history-meta {
        font-size: 0.7rem;
        color: #8a8f9c;
        margin-top: 0.2rem;
    }

    /* ===== PR Card ===== */
    .pr-card {
        background: linear-gradient(135deg, #1a1d27 0%, #1e2433 100%);
        border: 1.5px solid #4facfe;
        border-radius: 14px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
    }
    .pr-exercise {
        font-size: 0.85rem;
        font-weight: 700;
        color: #e8eaf0;
    }
    .pr-value {
        font-size: 0.75rem;
        color: #4facfe;
        font-weight: 600;
        margin-top: 0.2rem;
    }

    /* ===== Settings Row ===== */
    .settings-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #1a1d27;
        border: 1.5px solid #2a2e3a;
        border-radius: 14px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
    }
    .settings-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #e8eaf0;
    }
    .settings-value {
        font-size: 0.75rem;
        color: #8a8f9c;
    }

    /* ===== Checkbox ===== */
    .stCheckbox > label {
        color: #e8eaf0;
        font-size: 0.85rem;
    }

    /* ===== Radio ===== */
    .stRadio > label {
        color: #e8eaf0;
        font-size: 0.85rem;
    }
    .stRadio [role="radiogroup"] {
        gap: 0.3rem;
    }
    .stRadio [role="radiogroup"] label {
        background: #1a1d27;
        border: 1.5px solid #2a2e3a;
        border-radius: 12px;
        padding: 0.5rem 0.8rem;
        font-size: 0.8rem;
        color: #e8eaf0;
    }
    .stRadio [role="radiogroup"] label:has(input:checked) {
        border-color: #4facfe;
        background: #1e2433;
    }
</style>
"""

st.markdown(MOBILE_CSS, unsafe_allow_html=True)

# ============================================================
# DATA LOADING
# ============================================================
@st.cache_data
def load_workout_plan():
    """Load the workout plan from JSON file."""
    json_path = os.path.join(os.path.dirname(__file__), "workout_plan.json")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_week_exercises(plan, week_idx, day):
    """Get exercises for a specific week and day."""
    week = plan["weeks"][week_idx]
    return week["schedule"].get(day, [])


def parse_exercise(exercise_str):
    """Parse exercise string into structured data.
    Format: "25 Pullups" or "15/4 Bicep Curl" or "100 Pushups (Close Grip Pushup)"
    """
    text = exercise_str.strip()
    # Check for reps/sets format
    import re
    match = re.match(r"^(\d+)/(\d+)\s+(.+)$", text)
    if match:
        reps = int(match.group(1))
        sets = int(match.group(2))
        name = match.group(3).strip()
        return {"name": name, "reps": reps, "sets": sets, "type": "weighted", "raw": text}

    # Check for reps only format
    match = re.match(r"^(\d+)\s+(.+)$", text)
    if match:
        reps = int(match.group(1))
        name = match.group(2).strip()
        return {"name": name, "reps": reps, "sets": None, "type": "bodyweight", "raw": text}

    # Special instructions
    return {"name": text, "reps": None, "sets": None, "type": "instruction", "raw": text}


# ============================================================
# STATE MANAGEMENT
# ============================================================
def init_state():
    """Initialize session state."""
    if "workout_logs" not in st.session_state:
        st.session_state.workout_logs = {}
    if "current_week" not in st.session_state:
        st.session_state.current_week = 0
    if "current_tab" not in st.session_state:
        st.session_state.current_tab = "Today"
    if "selected_day" not in st.session_state:
        st.session_state.selected_day = None
    if "completed_exercises" not in st.session_state:
        st.session_state.completed_exercises = set()
    if "cardio_done" not in st.session_state:
        st.session_state.cardio_done = False
    if "weight_entries" not in st.session_state:
        st.session_state.weight_entries = {}
    if "db_initialized" not in st.session_state:
        st.session_state.db_initialized = False
    if "sync_status" not in st.session_state:
        st.session_state.sync_status = "Not synced"
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = None

    # Load data from ChromaDB on first run
    if not st.session_state.db_initialized:
        try:
            db = get_db()
            saved_logs = db.load_all_workout_logs()
            if saved_logs:
                st.session_state.workout_logs = saved_logs
                st.session_state.sync_status = f"Loaded {len(saved_logs)} saved workout(s)"
            st.session_state.db_initialized = True
        except Exception as e:
            st.session_state.sync_status = f"DB unavailable: {str(e)[:50]}"
            st.session_state.db_initialized = True


def get_today_key():
    """Get today's date key."""
    return date.today().isoformat()


def get_day_name():
    """Get today's day name."""
    return date.today().strftime("%A")


def save_workout_log(week_idx, day, exercises, cardio_done):
    """Save a workout log for a specific day."""
    key = f"{week_idx}|{day}"
    st.session_state.workout_logs[key] = {
        "date": get_today_key(),
        "week": week_idx,
        "day": day,
        "exercises": exercises,
        "cardio_done": cardio_done,
        "completed_at": datetime.now().isoformat(),
    }

    # Save to ChromaDB for persistence
    try:
        db = get_db()
        db.save_workout_log(
            week_idx=week_idx,
            day=day,
            exercises=list(exercises),
            cardio_done=cardio_done,
            weight_entries=st.session_state.weight_entries,
        )
        st.session_state.sync_status = f"Synced: {day} saved to database"
    except Exception as e:
        st.session_state.sync_status = f"Sync failed: {str(e)[:50]}"


def get_workout_log(week_idx, day):
    """Get workout log for a specific day."""
    key = f"{week_idx}|{day}"
    return st.session_state.workout_logs.get(key)


def is_day_completed(week_idx, day):
    """Check if a day's workout is completed."""
    log = get_workout_log(week_idx, day)
    return log is not None


# ============================================================
# UI COMPONENTS
# ============================================================
def render_header():
    """Render the app header."""
    today = date.today()
    formatted_date = today.strftime("%A, %B %d")
    st.markdown(
        f"""
        <div class="app-header">
            <div>
                <div class="app-title">💪 FitTrack</div>
                <div class="app-date">{formatted_date}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_week_selector(plan):
    """Render the week selector chips."""
    weeks = plan["weeks"]
    cols = st.columns(len(weeks))
    for i, week in enumerate(weeks):
        with cols[i]:
            is_active = st.session_state.current_week == i
            if st.button(
                week["week"].replace("Week ", "W"),
                key=f"week_{i}",
                use_container_width=True,
            ):
                st.session_state.current_week = i
                st.session_state.selected_day = None
                st.rerun()


def render_cardio_banner(plan):
    """Render the cardio banner for the current week."""
    week = plan["weeks"][st.session_state.current_week]
    cardio = week["cardio"]
    done = st.session_state.cardio_done
    status = "✅ Completed" if done else "⏱️ Pending"
    st.markdown(
        f"""
        <div class="cardio-banner">
            <div class="cardio-icon">🏃</div>
            <div>
                <div class="cardio-text">{cardio}</div>
                <div class="cardio-sub">{status}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_day_cards(plan):
    """Render the weekly day cards."""
    week = plan["weeks"][st.session_state.current_week]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today_name = get_day_name()

    for day in days:
        exercises = get_week_exercises(plan, st.session_state.current_week, day)
        is_today = day == today_name
        is_rest = any("Rest" in ex for ex in exercises)
        is_done = is_day_completed(st.session_state.current_week, day)

        # Build exercise summary
        if is_rest:
            summary = "🛌 Rest day"
        else:
            ex_count = len(exercises)
            summary = f"{ex_count} exercises"

        badge_class = "today" if is_today else ("done" if is_done else "")
        badge_text = "TODAY" if is_today else ("✓ DONE" if is_done else "")

        card_class = "day-card"
        if is_today:
            card_class += " today"
        if is_rest:
            card_class += " rest"

        st.markdown(
            f"""
            <div class="{card_class}" onclick="document.querySelector('[data-testid=\'stButton\']').click()">
                <div class="day-header">
                    <span class="day-name">{day}</span>
                    <span class="day-badge {badge_class}">{badge_text}</span>
                </div>
                <div class="day-exercises">{summary}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Hidden button for day selection
        if st.button(f"View {day}", key=f"day_{day}", use_container_width=True):
            st.session_state.selected_day = day
            st.rerun()


def render_today_view(plan):
    """Render the Today view - today's workout."""
    st.markdown('<div class="section-title">Today\'s Workout</div>', unsafe_allow_html=True)

    today_name = get_day_name()
    week = plan["weeks"][st.session_state.current_week]
    exercises = get_week_exercises(plan, st.session_state.current_week, today_name)

    # Cardio banner
    render_cardio_banner(plan)

    # Cardio checkbox
    cardio_done = st.checkbox("✅ Complete Cardio", value=st.session_state.cardio_done)
    st.session_state.cardio_done = cardio_done

    if not exercises:
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-icon">🎉</div>
                <div class="empty-text">Rest day!<br>Enjoy your recovery.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Check if rest day
    if any("Rest" in ex for ex in exercises):
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-icon">🛌</div>
                <div class="empty-text">Rest day!<br>Recovery is part of the plan.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Progress tracking
    completed_count = len(st.session_state.completed_exercises)
    total_count = len(exercises)
    progress = completed_count / total_count if total_count > 0 else 0

    st.markdown(
        f"""
        <div class="progress-ring">
            <div class="progress-percent">{int(progress * 100)}%</div>
            <div class="progress-label">{completed_count}/{total_count} exercises completed</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.progress(progress)

    # Exercise cards
    st.markdown('<div class="section-sub">Tap to mark exercises as completed</div>', unsafe_allow_html=True)

    for i, ex_str in enumerate(exercises):
        ex = parse_exercise(ex_str)
        is_completed = ex_str in st.session_state.completed_exercises

        # Build exercise display
        if ex["type"] == "weighted":
            meta = f"{ex['reps']} reps × {ex['sets']} sets"
        elif ex["type"] == "bodyweight":
            meta = f"{ex['reps']} reps"
        else:
            meta = ""

        card_class = "exercise-card" + (" completed" if is_completed else "")
        check_class = "exercise-check" + (" done" if is_completed else "")
        check_mark = "✓" if is_completed else ""

        st.markdown(
            f"""
            <div class="{card_class}">
                <div class="exercise-header">
                    <div>
                        <div class="exercise-name">{ex['name']}</div>
                        <div class="exercise-meta">{meta}</div>
                    </div>
                    <div class="{check_class}">{check_mark}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Toggle button
        if st.button(
            "✓ Mark Done" if not is_completed else "↩️ Undo",
            key=f"toggle_{i}_{ex_str}",
            use_container_width=True,
        ):
            if is_completed:
                st.session_state.completed_exercises.discard(ex_str)
            else:
                st.session_state.completed_exercises.add(ex_str)
            st.rerun()

    # Save workout button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 Save Workout", use_container_width=True):
        save_workout_log(
            st.session_state.current_week,
            today_name,
            list(st.session_state.completed_exercises),
            st.session_state.cardio_done,
        )
        st.success("Workout saved! 💪")


def render_plan_view(plan):
    """Render the Plan view - weekly schedule."""
    st.markdown('<div class="section-title">Workout Plan</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-sub">{plan["title"]} • {plan["weeks"][st.session_state.current_week]["week"]}</div>',
        unsafe_allow_html=True,
    )

    # Week selector
    render_week_selector(plan)

    # Cardio banner
    render_cardio_banner(plan)

    # Day cards
    render_day_cards(plan)

    # Selected day detail
    if st.session_state.selected_day:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f'<div class="section-title">{st.session_state.selected_day} Details</div>',
            unsafe_allow_html=True,
        )

        exercises = get_week_exercises(plan, st.session_state.current_week, st.session_state.selected_day)

        if any("Rest" in ex for ex in exercises):
            st.markdown(
                """
                <div class="empty-state">
                    <div class="empty-icon">🛌</div>
                    <div class="empty-text">Rest day!<br>Recovery is part of the plan.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for ex_str in exercises:
                ex = parse_exercise(ex_str)
                if ex["type"] == "weighted":
                    meta = f"{ex['reps']} reps × {ex['sets']} sets"
                elif ex["type"] == "bodyweight":
                    meta = f"{ex['reps']} reps"
                else:
                    meta = ""

                st.markdown(
                    f"""
                    <div class="exercise-card">
                        <div class="exercise-header">
                            <div>
                                <div class="exercise-name">{ex['name']}</div>
                                <div class="exercise-meta">{meta}</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def render_history_view(plan):
    """Render the History view - past workouts."""
    st.markdown('<div class="section-title">Workout History</div>', unsafe_allow_html=True)

    if not st.session_state.workout_logs:
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-icon">📋</div>
                <div class="empty-text">No workouts logged yet.<br>Complete a workout to see it here!</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Stats grid
    total_workouts = len(st.session_state.workout_logs)
    total_exercises = sum(len(log["exercises"]) for log in st.session_state.workout_logs.values())
    cardio_count = sum(1 for log in st.session_state.workout_logs.values() if log["cardio_done"])

    st.markdown(
        f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{total_workouts}</div>
                <div class="stat-label">Workouts</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{total_exercises}</div>
                <div class="stat-label">Exercises</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{cardio_count}</div>
                <div class="stat-label">Cardio</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # History cards (sorted by date, newest first)
    logs = sorted(
        st.session_state.workout_logs.items(),
        key=lambda x: x[1]["date"],
        reverse=True,
    )

    for key, log in logs:
        week_num = log["week"] + 1
        day = log["day"]
        ex_count = len(log["exercises"])
        cardio = "🏃" if log["cardio_done"] else ""
        date_str = log["date"]

        st.markdown(
            f"""
            <div class="history-card">
                <div class="history-date">{day} • Week {week_num} {cardio}</div>
                <div class="history-meta">{date_str} • {ex_count} exercises completed</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_coach_view(plan):
    """Render the Coach view - AI-powered workout recommendations."""
    st.markdown('<div class="section-title">AI Coach</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Personalized next month recommendations based on your logged data</div>',
        unsafe_allow_html=True,
    )

    # Generate or load recommendations
    if st.session_state.recommendations is None:
        try:
            db = get_db()
            st.session_state.recommendations = db.generate_recommendations(
                st.session_state.workout_logs,
                plan
            )
        except Exception as e:
            st.error(f"Could not generate recommendations: {str(e)[:80]}")
            return

    rec = st.session_state.recommendations

    # Summary card
    completed = rec.get("completed_workouts", 0)
    if completed == 0:
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-icon">🤖</div>
                <div class="empty-text">Start logging workouts to get<br>personalized AI recommendations!</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Stats
    st.markdown(
        f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{rec.get('completed_workouts', 0)}</div>
                <div class="stat-label">Workouts</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{rec.get('total_exercises', 0)}</div>
                <div class="stat-label">Exercises</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{rec.get('cardio_count', 0)}</div>
                <div class="stat-label">Cardio</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Insights
    insights = rec.get("insights", [])
    if insights:
        st.markdown('<div class="section-sub">📊 Your Patterns</div>', unsafe_allow_html=True)
        for insight in insights:
            st.markdown(
                f"""
                <div class="history-card">
                    <div class="history-date">💡 {insight}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Recommendations
    recommendations = rec.get("recommendations", [])
    if recommendations:
        st.markdown('<div class="section-sub">🤖 AI Recommendations</div>', unsafe_allow_html=True)
        for i, rec_text in enumerate(recommendations, 1):
            st.markdown(
                f"""
                <div class="pr-card">
                    <div class="pr-exercise">📌 {i}. {rec_text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Next month plan
    next_plan = rec.get("next_month_plan", "")
    if next_plan:
        st.markdown('<div class="section-sub">🗓️ Next Month Plan</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="cardio-banner">
                <div class="cardio-icon">📋</div>
                <div>
                    <div class="cardio-text">{next_plan}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Refresh button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Recommendations", use_container_width=True):
        try:
            db = get_db()
            st.session_state.recommendations = db.generate_recommendations(
                st.session_state.workout_logs,
                plan
            )
            st.rerun()
        except Exception as e:
            st.error(f"Could not refresh: {str(e)[:80]}")


def render_progress_view(plan):
    """Render the Progress view - charts and PRs."""
    st.markdown('<div class="section-title">Progress</div>', unsafe_allow_html=True)

    if not st.session_state.workout_logs:
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-icon">📊</div>
                <div class="empty-text">No progress data yet.<br>Log workouts to see your progress!</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Weekly completion stats
    st.markdown('<div class="section-sub">Weekly Completion</div>', unsafe_allow_html=True)

    week_completion = {}
    for key, log in st.session_state.workout_logs.items():
        week_num = log["week"] + 1
        if week_num not in week_completion:
            week_completion[week_num] = {"days": 0, "exercises": 0}
        week_completion[week_num]["days"] += 1
        week_completion[week_num]["exercises"] += len(log["exercises"])

    # Display weekly stats
    cols = st.columns(len(week_completion) if week_completion else 1)
    for i, (week_num, stats) in enumerate(sorted(week_completion.items())):
        with cols[i]:
            st.metric(
                label=f"Week {week_num}",
                value=f"{stats['days']} days",
                delta=f"{stats['exercises']} exercises",
            )

    # Exercise completion breakdown
    st.markdown('<div class="section-sub">Exercise Completion</div>', unsafe_allow_html=True)

    exercise_counts = {}
    for key, log in st.session_state.workout_logs.items():
        for ex in log["exercises"]:
            parsed = parse_exercise(ex)
            name = parsed["name"]
            if name not in exercise_counts:
                exercise_counts[name] = 0
            exercise_counts[name] += 1

    if exercise_counts:
        # Sort by count descending
        sorted_exercises = sorted(exercise_counts.items(), key=lambda x: x[1], reverse=True)
        for name, count in sorted_exercises[:10]:
            st.markdown(
                f"""
                <div class="history-card">
                    <div class="history-date">{name}</div>
                    <div class="history-meta">Completed {count} time{'s' if count != 1 else ''}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Personal Records
    st.markdown('<div class="section-sub">Personal Records</div>', unsafe_allow_html=True)

    # Track PRs from weight entries
    if st.session_state.weight_entries:
        for exercise, weight in sorted(st.session_state.weight_entries.items()):
            st.markdown(
                f"""
                <div class="pr-card">
                    <div class="pr-exercise">🏆 {exercise}</div>
                    <div class="pr-value">Best: {weight} kg</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-icon">🏆</div>
                <div class="empty-text">No personal records yet.<br>Log weighted exercises to track PRs!</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_settings_view(plan):
    """Render the Settings view."""
    st.markdown('<div class="section-title">Settings</div>', unsafe_allow_html=True)

    # Plan info
    st.markdown(
        f"""
        <div class="settings-row">
            <div class="settings-label">📋 Plan</div>
            <div class="settings-value">{plan['title']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Current week
    st.markdown(
        f"""
        <div class="settings-row">
            <div class="settings-label">📅 Current Week</div>
            <div class="settings-value">{plan['weeks'][st.session_state.current_week]['week']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Cloud sync status
    st.markdown('<div class="section-sub">Cloud Sync</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="settings-row">
            <div class="settings-label">☁️ Sync Status</div>
            <div class="settings-value">{st.session_state.sync_status}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("🔄 Sync Now", use_container_width=True):
        try:
            db = get_db()
            for key, log in st.session_state.workout_logs.items():
                db.save_workout_log(
                    week_idx=log.get("week", 0),
                    day=log.get("day", ""),
                    exercises=log.get("exercises", []),
                    cardio_done=log.get("cardio_done", False),
                    weight_entries=log.get("weight_entries", {}),
                )
            st.session_state.sync_status = f"Synced {len(st.session_state.workout_logs)} workout(s) to cloud"
            st.success("Cloud sync complete! ✅")
        except Exception as e:
            st.session_state.sync_status = f"Sync failed: {str(e)[:50]}"
            st.error(f"Sync failed. Will retry when online: {str(e)[:80]}")

    # Data management
    st.markdown('<div class="section-sub">Data Management</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Export Data", use_container_width=True):
            export_data = {
                "workout_logs": st.session_state.workout_logs,
                "completed_exercises": list(st.session_state.completed_exercises),
                "weight_entries": st.session_state.weight_entries,
                "exported_at": datetime.now().isoformat(),
            }
            st.download_button(
                label="⬇️ Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"fittrack_export_{get_today_key()}.json",
                mime="application/json",
                use_container_width=True,
            )

    with col2:
        if st.button("🗑️ Clear All Data", use_container_width=True):
            st.session_state.workout_logs = {}
            st.session_state.completed_exercises = set()
            st.session_state.weight_entries = {}
            st.session_state.cardio_done = False
            st.rerun()

    # About
    st.markdown('<div class="section-sub">About</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="settings-row">
            <div class="settings-label">ℹ️ Version</div>
            <div class="settings-value">1.0.0</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="settings-row">
            <div class="settings-label">💪 FitTrack</div>
            <div class="settings-value">Personal Fitness Tracker</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_bottom_nav():
    """Render the bottom navigation bar using Streamlit buttons."""
    tabs = [
        ("Today", "📅"),
        ("Plan", "📋"),
        ("Progress", "📈"),
        ("Coach", "🤖"),
        ("Settings", "⚙️"),
    ]

    # Use Streamlit buttons styled as bottom nav
    cols = st.columns(len(tabs))
    for i, (tab_name, icon) in enumerate(tabs):
        with cols[i]:
            is_active = st.session_state.current_tab == tab_name
            label = f"{icon}\n\n{tab_name}"
            if st.button(
                label,
                key=f"nav_{tab_name}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.current_tab = tab_name
                st.rerun()


# ============================================================
# MAIN APP
# ============================================================
def main():
    """Main application entry point."""
    init_state()

    # Load workout plan
    plan = load_workout_plan()

    # Render header
    render_header()

    # Render main content based on current tab
    if st.session_state.current_tab == "Today":
        render_today_view(plan)
    elif st.session_state.current_tab == "Plan":
        render_plan_view(plan)
    elif st.session_state.current_tab == "Progress":
        render_progress_view(plan)
    elif st.session_state.current_tab == "Coach":
        render_coach_view(plan)
    elif st.session_state.current_tab == "Settings":
        render_settings_view(plan)

    # Render bottom navigation
    render_bottom_nav()


if __name__ == "__main__":
    main()