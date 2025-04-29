import streamlit as st
from ai import configure_genai, generate_code, build_system_prompt

st.set_page_config(page_title="Code Assistant", page_icon="💻", layout="wide")

st.sidebar.title("⚙️ Settings")
language = st.sidebar.selectbox("Language", ["Python", "JavaScript", "Java", "C++", "C"])
user_api_key = st.sidebar.text_input("🔑 Gemini API Key (optional)", type="password")

model = configure_genai(user_api_key)

st.markdown("""
<style>
body { background-color: #0e1117; color: #c9d1d9; }
.stTextArea textarea { background-color: #161b22; color: #c9d1d9; }
.stButton button { background-color: #238636; color: white; border-radius: 8px; height: 3em; width: 100%; font-size: 1.1em; }
.stMarkdown code { background-color: #161b22; color: #c9d1d9; }
</style>
""", unsafe_allow_html=True)

st.title("💻 Code Generation Assistant")
st.write("Enter a coding request. Language is selected via the dropdown.")

if "conversation" not in st.session_state:
    st.session_state.conversation = []

user_input = st.text_area("Your coding request:", height=150, placeholder="e.g., Write a function to check for palindromes.")

if st.button("🔄 Generate Code") and user_input:
    with st.spinner("Generating code..."):
        system_prompt = build_system_prompt(language)
        output = generate_code(model, user_input, system_prompt)
        st.session_state.conversation.append({"role": "user", "content": user_input})
        st.session_state.conversation.append({"role": "assistant", "content": output})

if st.session_state.conversation:
    for entry in st.session_state.conversation:
        if entry['role'] == 'user':
            st.markdown(f"**You:** {entry['content']}")
        else:
            st.markdown("**Assistant:**")
            st.code(entry['content'].strip('`'), language=language.lower())
