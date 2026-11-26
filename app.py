import json
import os
from datetime import datetime

import streamlit as st
from graph import graph

st.set_page_config(
    page_title="Multi-Agent Business Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

THEMES = {
    "Lavender (Default)": dict(
        ink="#1E1B4B", bg_top="#F8F8FE", bg_bot="#FFFFFF", blob="#E4E4F8", card="#FFFFFF",
        card_border="#ECECF8", soft="#EEEEFA", border="#D5D5EE", side="#F1F1FB",
        btn="#1E1B4B", btn_hover="#2E2A6B", btn_text="#FFFFFF", icon="#EDEDFA",
        spark="#5B5F97", shadow="rgba(30,27,75,0.08)"),
    "Olive & White": dict(
        ink="#2B2B2B", bg_top="#FAFBF5", bg_bot="#FFFFFF", blob="#E8ECD8", card="#FFFFFF",
        card_border="#E6EAD6", soft="#F1F3E8", border="#D3D9BC", side="#F1F3E8",
        btn="#556B2F", btn_hover="#445724", btn_text="#FFFFFF", icon="#E8ECD8",
        spark="#7C8F55", shadow="rgba(85,107,47,0.10)"),
    "Soft Glam": dict(
        ink="#3A2A30", bg_top="#FFF5F7", bg_bot="#FFFFFF", blob="#FCE4EC", card="#FFFFFF",
        card_border="#F8DCE5", soft="#FDEBF0", border="#F3C6D6", side="#FCE4EC",
        btn="#C2185B", btn_hover="#A5124C", btn_text="#FFFFFF", icon="#FCE4EC",
        spark="#D6708F", shadow="rgba(194,24,91,0.10)"),
    "Dark Pro": dict(
        ink="#E2E8F0", bg_top="#0F172A", bg_bot="#0B1222", blob="#1E293B", card="#1E293B",
        card_border="#334155", soft="#0F172A", border="#334155", side="#111B2E",
        btn="#38BDF8", btn_hover="#0EA5E9", btn_text="#0F172A", icon="#334155",
        spark="#38BDF8", shadow="rgba(0,0,0,0.40)"),
}

# ---------------- History (saved in history.json) ----------------
HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history.json")
MAX_HISTORY = 20

def load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_history(items):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
    except OSError:
        pass

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Settings")
    theme_name = st.selectbox("Theme", list(THEMES.keys()))
    st.markdown("---")
    st.markdown("**Agents**")
    st.markdown("1. Research Agent\n2. Report Agent")
    st.markdown("---")
    st.markdown("**History**")
    history = load_history()
    if not history:
        st.caption("No searches yet.")
    for i, item in enumerate(history):
        label = item["topic"] if len(item["topic"]) <= 28 else item["topic"][:28] + "..."
        if st.button(label, key=f"hist_{i}", help=item.get("time", ""), use_container_width=True):
            st.session_state.current = item
    if history and st.button("Clear history", key="clear_hist"):
        save_history([])
        st.session_state.pop("current", None)
        st.rerun()

t = THEMES[theme_name]

# ---------------- Styling ----------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap');

html, body, .stApp, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

.stApp {{
    background:
        radial-gradient(circle at 0% 15%, {t['blob']} 0%, transparent 32%),
        radial-gradient(circle at 100% 5%, {t['blob']} 0%, transparent 28%),
        radial-gradient(circle at 100% 100%, {t['blob']} 0%, transparent 30%),
        linear-gradient(180deg, {t['bg_top']} 0%, {t['bg_bot']} 100%);
    color: {t['ink']};
}}
#MainMenu, footer {{ visibility: hidden; }}
header[data-testid="stHeader"] {{ background: transparent; }}

/* Sidebar */
[data-testid="stSidebar"] {{ background: {t['side']}; border-right: 1px solid {t['card_border']}; }}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] li,
[data-testid="stSidebar"] span, [data-testid="stSidebar"] small {{ color: {t['ink']}; }}
[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
    background: {t['soft']}; border: 1px solid {t['border']}; border-radius: 10px; color: {t['ink']};
}}
[data-testid="stSidebar"] div[data-baseweb="select"] * {{ color: {t['ink']} !important; }}

[data-testid="stSidebar"] .stButton button {{
    background: {t['soft']}; color: {t['ink']}; border: 1px solid {t['border']};
    border-radius: 10px; justify-content: flex-start; text-align: left;
}}
[data-testid="stSidebar"] .stButton button:hover {{ border-color: {t['btn']}; color: {t['ink']}; }}
[data-testid="stSidebar"] .stButton button p {{ color: {t['ink']}; }}

/* Hero */
.hero {{ text-align: center; margin-top: 0.5rem; }}
.hero h1 {{ font-size: 2.4rem; font-weight: 800; color: {t['ink']}; margin: 0.4rem 0 0.2rem 0; }}
.hero p {{ font-size: 1.05rem; color: {t['ink']}; opacity: 0.85; margin-bottom: 1.6rem; }}

.sparkle {{ position: fixed; color: {t['spark']}; opacity: 0.6; font-size: 1.6rem; z-index: 0; }}

/* Input card */
div[data-testid="stForm"] {{
    background: {t['card']};
    border: 1px solid {t['card_border']};
    border-radius: 22px;
    padding: 1.4rem 1.6rem 1.6rem 1.6rem;
    box-shadow: 0 10px 30px {t['shadow']};
}}
div[data-testid="stForm"] label p {{ font-weight: 600; color: {t['ink']}; }}
div[data-testid="stForm"] div[data-baseweb="input"] > div {{
    background: {t['soft']}; border: 1px solid {t['border']}; border-radius: 12px;
}}
div[data-testid="stForm"] div[data-baseweb="input"] input {{
    color: {t['ink']}; padding: 0.7rem 0.9rem;
}}

/* Generate button */
div[data-testid="stFormSubmitButton"] {{ display: flex; justify-content: center; }}
div[data-testid="stFormSubmitButton"] button {{
    background: {t['btn']}; color: {t['btn_text']}; border: none; border-radius: 12px;
    padding: 0.7rem 2.2rem; font-weight: 600; font-size: 1rem;
}}
div[data-testid="stFormSubmitButton"] button:hover {{ background: {t['btn_hover']}; color: {t['btn_text']}; }}
div[data-testid="stFormSubmitButton"] button p {{ color: {t['btn_text']}; }}

/* Feature row */
.features {{ display: flex; justify-content: center; gap: 2.2rem; margin: 1.8rem 0 1rem 0; flex-wrap: wrap; }}
.feature {{ display: flex; align-items: center; gap: 0.7rem; font-weight: 500; line-height: 1.25; color: {t['ink']}; }}
.icon {{
    width: 46px; height: 46px; border-radius: 50%; background: {t['icon']};
    display: flex; align-items: center; justify-content: center; font-size: 1.3rem;
}}

/* Main area text */
.block-container h3, .block-container p, .block-container li {{ color: {t['ink']}; }}

/* Result card */
.report-card {{
    background: {t['card']}; border: 1px solid {t['card_border']}; border-radius: 18px;
    padding: 1.4rem 1.6rem; box-shadow: 0 10px 30px {t['shadow']};
}}
</style>

<div class="sparkle" style="top:28%; left:26%;">✦</div>
<div class="sparkle" style="top:34%; left:23%; font-size:1.1rem;">✦</div>
<div class="sparkle" style="top:30%; right:6%;">✦</div>
<div class="sparkle" style="top:35%; right:3.5%; font-size:1.1rem;">✦</div>
""", unsafe_allow_html=True)

# ---------------- Hero ----------------
st.markdown(f"""
<div class="hero">
  <svg width="120" height="110" viewBox="0 0 120 110" xmlns="http://www.w3.org/2000/svg">
    <line x1="60" y1="6" x2="60" y2="20" stroke="{t['ink']}" stroke-width="4" stroke-linecap="round"/>
    <circle cx="60" cy="6" r="5" fill="{t['ink']}"/>
    <rect x="22" y="40" width="10" height="26" rx="5" fill="{t['card']}" stroke="{t['ink']}" stroke-width="3"/>
    <rect x="88" y="40" width="10" height="26" rx="5" fill="{t['card']}" stroke="{t['ink']}" stroke-width="3"/>
    <rect x="28" y="20" width="64" height="68" rx="30" fill="{t['card']}" stroke="{t['ink']}" stroke-width="4"/>
    <rect x="38" y="36" width="44" height="32" rx="14" fill="{t['ink']}"/>
    <circle cx="51" cy="50" r="5" fill="{t['card']}"/>
    <circle cx="69" cy="50" r="5" fill="{t['card']}"/>
    <path d="M52 59 Q60 65 68 59" stroke="{t['card']}" stroke-width="3" fill="none" stroke-linecap="round"/>
  </svg>
  <h1>Multi-Agent Business Assistant</h1>
  <p>Enter a topic. Agents research the web and write a professional report.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- Input card ----------------
with st.form("topic_form"):
    topic = st.text_input("🎯 Topic", placeholder="e.g. Online clothing market in Pakistan")
    submitted = st.form_submit_button("➤  Generate Report")

# ---------------- Feature row ----------------
st.markdown("""
<div class="features">
  <div class="feature"><div class="icon">🔍</div><div>Research<br>Automatically</div></div>
  <div class="feature"><div class="icon">📄</div><div>Get Professional<br>Reports</div></div>
  <div class="feature"><div class="icon">⚡</div><div>Powered by<br>Multi-Agent AI</div></div>
</div>
""", unsafe_allow_html=True)

# ---------------- Run agents ----------------
if submitted:
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        research, report = "", ""
        try:
            with st.status("Agents are working...", expanded=True) as status:
                state = {"topic": topic.strip(), "research": "", "report": ""}
                for update in graph.stream(state, stream_mode="updates"):
                    for node, out in update.items():
                        if node == "research":
                            research = out["research"]
                            st.write("✅ Research Agent finished")
                        elif node == "report":
                            report = out["report"]
                            st.write("✅ Report Agent finished")
                status.update(label="Report ready", state="complete")

            item = {
                "topic": topic.strip(),
                "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                "research": research,
                "report": report,
            }
            saved = load_history()
            saved.insert(0, item)
            save_history(saved[:MAX_HISTORY])
            st.session_state.current = item
            st.rerun()
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# ---------------- Show current / selected report ----------------
current = st.session_state.get("current")
if current:
    st.markdown(f"### Report: {current['topic']}")
    if current.get("time"):
        st.caption(current["time"])
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    st.markdown(current["report"])
    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("View research used"):
        st.write(current["research"])
    st.download_button("Download report", current["report"], file_name="report.md")