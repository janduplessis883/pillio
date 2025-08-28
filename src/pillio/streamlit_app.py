import streamlit as st

from support.support_ui import color_message_box, gradient_border_box
from support.support_supabase import get_todos, add_todo, delete_todo, sign_up, sign_in, sign_out, update_todo
from support.support_app import auth_screen

st.set_page_config(page_title="Pillio - Medication Alerts: Brompton Health PCN", page_icon=":material/pill:", layout="centered")
st.logo("images/pillio_logo.png", size="large")


def main_app(user_name):
    st.sidebar.title(":material/assistant_navigation: Navigation")
    c1, c2 = st.columns([4, 1])
    with c1:
        gradient_border_box(f"Welcome, {user_name} 😊!")
    with c2:
        if st.button("Logout"):
            sign_out()



if "user_email" not in st.session_state:
    st.session_state.user_email = None
    st.session_state.user_name = None

if st.session_state.user_email:
    main_app(st.session_state.get('user_name', st.session_state.user_email))
else:
    auth_screen()
