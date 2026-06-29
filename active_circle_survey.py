import streamlit as st
from utils import save_response
from datetime import datetime

st.set_page_config(page_title="Active Circle Survey", page_icon=":clipboard:", layout="centered")

# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'responses' not in st.session_state:
    st.session_state.responses = {}

# Configure branding
st.markdown("""
<style>
body {
    background-color: #FAF7F2;
    font-family: 'Inter', sans-serif;
}
.question-number {
    color: #DF577B;
    font-weight: bold;
}
.question-text {
    color: #2E2A2B;
    font-family: 'Inter', sans-serif;
}
.italic-text {
    color: #2E2A2B;
    font-style: italic;
    font-family: 'Inter', sans-serif;
}
div[data-testid="stButton"] button {
    background-color: #DF577B !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 600 !important;
    padding: 8px 16px !important;
}
div[data-testid="stButton"] button:hover {
    background-color: #c94668 !important;
}
</style>
""", unsafe_allow_html=True)

st.image("assets/Banner.png", width=700)

questions = [
    {
        "main": "What is your biggest challenge in life right now?",
        "subtitle": "Please be as detailed as possible. The more specific and detailed you are, the more likely I´ll be able to support you."
    },
    {
        "main": "Why do you think this is happening?",
        "subtitle": None
    },
    {
        "main": "How is this affecting your daily life?",
        "subtitle": None
    },
    {
        "main": "What would meaningful support look like for you?",
        "subtitle": None
    }
]

def render_question():
    question_num = st.session_state.current_question + 1
    question = questions[st.session_state.current_question]
    
    # Display question number and main text on the same line
    st.markdown(f"<p class='question-text'><span class='question-number'>{question_num}.</span> {question['main']}</p>", unsafe_allow_html=True)
    
    # Display subtitle if it exists
    if question['subtitle']:
        st.markdown(f"<p class='italic-text'>{question['subtitle']}</p>", unsafe_allow_html=True)
    
    # Text area for answer
    placeholder = "Type your answer here…"
    response = st.text_area(
        label="",
        value=st.session_state.responses.get(st.session_state.current_question, ""),
        height=200,
        max_chars=3000,
        placeholder=placeholder,
        key=f"answer_{st.session_state.current_question}"
    )
    
    st.session_state.responses[st.session_state.current_question] = response

def render_navigation():
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col3:
        if st.session_state.current_question < len(questions) - 1:
            if st.button("Next »", key="next_btn", use_container_width=True):
                st.session_state.current_question += 1
                st.rerun()
        else:
            if st.button("Next »", key="next_btn", use_container_width=True):
                st.session_state.current_question += 1
                st.rerun()
    
    with col2:
        if st.session_state.current_question > 0:
            if st.button("« Back", key="back_btn", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()

def render_contact_form():
    st.markdown("### Contact Information")
    st.markdown("Lastly, I may want to follow up with a few people personally to learn more about your situation. If you´d be open to chatting for a few minutes (promise not to sell you anything), please leave your contact information below. If not, you can click 'Submit' to end the survey :)")
    
    name = st.text_input("Name", key="name_input")
    phone = st.text_input("Phone", key="phone_input")
    email = st.text_input("Email", key="email_input")
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col3:
        if st.button("Submit", key="submit_btn", use_container_width=True):
            save_response(st.session_state.responses, name, phone, email, circle="Active")
            st.success("Thank you for completing the survey! Redirecting...")
            st.markdown(f"<meta http-equiv='refresh' content='2;url=https://morella-devost.mykajabi.com/deep-dive-survey-thank-you?preview_theme_id=2166678693' />", unsafe_allow_html=True)
    
    with col2:
        if st.button("« Back", key="back_contact_btn", use_container_width=True):
            st.session_state.current_question -= 1
            st.rerun()

# Main flow
if st.session_state.current_question < len(questions):
    render_question()
    render_navigation()
else:
    render_contact_form()
