import streamlit as st
import pandas as pd

from support.support_ui import gradient_border_box
from support.support_supabase import (
    get_alerts,
    get_surgeries,
    get_actions,
    sign_up,
    sign_in,
    sign_out
)
from support.support_app import auth_screen, manage_surgeries_page, manage_users_page, view_dataframes

st.set_page_config(page_title="Pillio - Drug Alerts: Brompton Health PCN", page_icon=":material/pill:", layout="wide")
st.logo("images/pillio_logo.png", size="large")


def main_app(user_name):

    with st.sidebar:
        gradient_border_box(f"Welcome, {user_name} 😊!")

        if st.button("Logout"):
            sign_out()
        st.divider()
        st.title(":material/assistant_navigation: Navigation")

        menu_options = ["Alerts", "View Dataframes"]

        # Show management pages only to administrators
        if st.session_state.get('user_role') == 'administrator':
            menu_options.insert(1, "Manage Surgeries")
            menu_options.append("Manage Users")

        menu_selection = st.sidebar.radio("Main Menu", menu_options, label_visibility="hidden")

    if menu_selection == "Alerts":
        st.header("Alerts Dashboard")
        st.info("Alerts functionality to be implemented.")

    elif menu_selection == "Manage Surgeries":
        manage_surgeries_page()

    elif menu_selection == "View Dataframes":
        view_dataframes()

    elif menu_selection == "Manage Users":
        manage_users_page()

if "user_email" not in st.session_state:
    st.session_state.user_email = None
    st.session_state.user_name = None
    st.session_state.user_role = None

if st.session_state.user_email:
    main_app(st.session_state.get('user_name', st.session_state.user_email))
else:
    auth_screen()
