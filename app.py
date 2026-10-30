import os

import streamlit as st
from groq import Groq

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Model names change over time. Check https://console.groq.com/docs/models
DEFAULT_MODEL = "openai/gpt-oss-120b"

st.set_page_config(
    page_title="AI Learning Roadmap Generator",
    page_icon="🗺️",
    layout="centered",
)


def get_api_key() -> str | None:
    """Read the Groq key from the environment/.env, then Streamlit secrets."""
    key = os.getenv("GROQ_API_KEY")
    if key:
        return key
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return None


def build_prompt(field, level, duration, unit, hours_per_week) -> str:
    return f"""Create a detailed, realistic learning roadmap.

Field: {field}
Current skill level: {level}
Total time available: {duration} {unit}
Study hours per week: {hours_per_week}

Format the answer in Markdown with these sections:
1. Overview and end goal (2-3 sentences)
2. Phase-by-phase (or week-by-week) plan that fits the time available exactly
3. For each phase: key topics, a hands-on mini project, and estimated hours
4. Recommended free resources (courses, documentation, books, YouTube channels)
5. A final capstone project idea
6. Tips to stay consistent and avoid common mistakes

Tailor the depth to a {level} learner and skip what they already know."""


def stream_roadmap(client: Groq, model: str, prompt: str):
    """Yield text chunks from Groq so Streamlit can render them live."""
    stream = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert mentor who designs realistic, "
                    "well-structured learning roadmaps."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.6,
        max_tokens=3000,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


# ---------------------------- UI ----------------------------

st.title("🗺️ AI Learning Roadmap Generator")
st.caption("Tell me what you want to learn and I'll build a plan that fits your time.")

with st.sidebar:
    st.header("Settings")
    model = st.text_input("Groq model", value=os.getenv("GROQ_MODEL", DEFAULT_MODEL))
    st.markdown("Get a free API key at [console.groq.com](https://console.groq.com).")

with st.form("roadmap_form"):
    field = st.text_input(
        "What do you want to learn?",
        placeholder="e.g. Machine Learning, Web Development, Cybersecurity",
    )
    level = st.selectbox("Your current level", ["Beginner", "Intermediate", "Advanced"])

    col1, col2, col3 = st.columns(3)
    duration = col1.number_input("Duration", min_value=1, max_value=52, value=3)
    unit = col2.selectbox("Unit", ["weeks", "months"], index=1)
    hours = col3.number_input("Hours / week", min_value=1, max_value=60, value=8)

    submitted = st.form_submit_button("Generate Roadmap", use_container_width=True)

if submitted:
    api_key = get_api_key()
    if not field.strip():
        st.warning("Please enter a field to learn.")
    elif not api_key:
        st.error(
            "GROQ_API_KEY not found. Add it to a .env file locally "
            "or to Streamlit secrets when deployed."
        )
    else:
        client = Groq(api_key=api_key)
        prompt = build_prompt(field.strip(), level, duration, unit, hours)
        try:
            st.subheader(f"Your {field.strip()} roadmap")
            roadmap = st.write_stream(stream_roadmap(client, model, prompt))
            st.session_state["roadmap"] = roadmap
            st.session_state["field"] = field.strip()
        except Exception as e:
            st.error(f"Something went wrong: {e}")
elif "roadmap" in st.session_state:
    st.subheader(f"Your {st.session_state['field']} roadmap")
    st.markdown(st.session_state["roadmap"])

if "roadmap" in st.session_state:
    st.download_button(
        "Download as Markdown",
        st.session_state["roadmap"],
        file_name=f"{st.session_state['field'].replace(' ', '_')}_roadmap.md",
        mime="text/markdown",
    )
