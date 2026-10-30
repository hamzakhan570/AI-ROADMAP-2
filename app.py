import streamlit as st
from roadmap import generate_roadmap

st.set_page_config(page_title="AI Learning Roadmap Generator", page_icon="🗺️", layout="centered")

st.title("🗺️ AI Learning Roadmap Generator")
st.caption("Tell me what you want to learn and I'll build your plan.")

with st.form("roadmap_form"):
    field = st.text_input("What do you want to learn?", placeholder="e.g. Machine Learning, Web Development")
    level = st.selectbox("Your current level", ["Beginner", "Intermediate", "Advanced"])

    col1, col2, col3 = st.columns(3)
    duration = col1.number_input("Duration", min_value=1, max_value=52, value=3)
    unit = col2.selectbox("Unit", ["weeks", "months"], index=1)
    hours = col3.number_input("Hours/week", min_value=1, max_value=60, value=8)

    submitted = st.form_submit_button("Generate Roadmap")

if submitted:
    if not field.strip():
        st.warning("Please enter a field to learn.")
    else:
        with st.spinner("Building your roadmap..."):
            try:
                result = generate_roadmap(field.strip(), level, duration, unit, hours)
                st.session_state["roadmap"] = result
                st.session_state["field"] = field.strip()
            except Exception as e:
                st.error(f"Something went wrong: {e}")

if "roadmap" in st.session_state:
    st.markdown(st.session_state["roadmap"])
    st.download_button(
        "Download as Markdown",
        st.session_state["roadmap"],
        file_name=f"{st.session_state['field'].replace(' ', '_')}_roadmap.md",
        mime="text/markdown",
    )
