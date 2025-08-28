import streamlit as st

from support.support_ui import color_message_box, gradient_border_box
from support.support_supabase import get_todos, add_todo, delete_todo, sign_up, sign_in, sign_out, update_todo


def auth_screen():
    st.image("images/pillio.png")

    c1,c2,c3 = st.columns([1,2,1])

    with c2:
        option = st.selectbox("Choose an action:", ["Login", "Sign Up"])


        if option == "Sign Up":
            name = st.text_input("Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Register"):
                user = sign_up(email, password, name)
                if user and user.user:
                    st.success("Registration successful! You can now log in.")
        else:
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                user = sign_in(email, password)
                if user and user.user:
                    st.session_state.user_email = user.user.email
                    st.session_state.user_name = user.user.user_metadata.get('full_name', 'Friend')
                    st.rerun()
