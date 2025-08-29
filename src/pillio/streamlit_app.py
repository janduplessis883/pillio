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
from support.support_app import auth_screen, manage_surgeries_page, manage_users_page

st.set_page_config(page_title="Pillio - Medication Alerts: Brompton Health PCN", page_icon=":material/pill:", layout="wide")
st.logo("images/pillio_logo.png", size="large")

def view_dataframes():
    """Fetches and displays all three dataframes."""
    st.header("Database Tables")

    st.subheader("Alerts")
    alerts_data = get_alerts()
    if alerts_data:
        df_alerts = pd.DataFrame(alerts_data)
        st.dataframe(df_alerts)
    else:
        st.info("No alerts data to display.")

    st.subheader("Surgeries")
    surgeries_data = get_surgeries()
    if surgeries_data:
        df_surgeries = pd.DataFrame(surgeries_data)
        st.dataframe(df_surgeries)
    else:
        st.info("No surgeries data to display.")

    st.subheader("Actions")
    actions_data = get_actions()
    if actions_data:
        df_actions = pd.DataFrame(actions_data)
        st.dataframe(df_actions)
    else:
        st.info("No actions data to display.")

def main_app(user_name):
    """Defines the main application layout and logic after login."""
    st.sidebar.title(":material/assistant_navigation: Navigation")

    menu_options = ["Alerts", "View Dataframes"]

    # Show management pages only to administrators
    if st.session_state.get('user_role') == 'administrator':
        menu_options.insert(1, "Manage Surgeries")
        menu_options.append("Manage Users")

    menu_selection = st.sidebar.radio("Main Menu", menu_options, label_visibility="hidden")

    c1, c2 = st.columns([4, 1])
    with c1:
        gradient_border_box(f"Welcome, {user_name} 😊!")
    with c2:
        if st.button("Logout"):
            sign_out()

    st.divider()

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
