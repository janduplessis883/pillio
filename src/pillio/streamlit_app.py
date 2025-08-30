import streamlit as st
import pandas as pd

from support.support_ui import gradient_border_box, alert_card
from support.support_supabase import (
    get_alerts,
    get_surgeries,
    get_actions,
    get_all_profiles,
    sign_up,
    sign_in,
    sign_out
)
from support.support_app import auth_screen, manage_surgeries_page, manage_users_page, manage_actions_page, view_dataframes

st.set_page_config(page_title="Pillio - Drug Alerts: Brompton Health PCN", page_icon=":material/pill:", layout="wide")
st.logo("images/pillio_logo.png", size="large")


def main_app(user_name):

    with st.sidebar:
        gradient_border_box(f"Welcome, {user_name} 😊!")

        if st.button("Logout"):
            sign_out()
        st.divider()
        st.header(":material/assistant_navigation: Navigation")

        menu_options = ["Alerts", "View Dataframes"]

        # Show management pages only to administrators
        if st.session_state.get('user_role') == 'administrator':
            menu_options.insert(1, "Manage Surgeries")
            menu_options.insert(2, "Manage Actions")
            menu_options.append("Manage Users")

        menu_selection = st.sidebar.radio("Main Menu", menu_options, label_visibility="hidden")

    if menu_selection == "Alerts":
        st.header("Alerts Dashboard")
        alerts = get_alerts()
        if alerts:

            for alert in alerts:
                alert_card(alert['title'], alert['issue_date'], alert['source'], alert['alert_refernce'])

                with st.popover("More Info", icon=":material/info:"):
                    st.write(f"**Description:** {alert.get('description', 'N/A')}")
                    st.write(f"**Severity:** {alert.get('severity', 'N/A')}")
                    st.write(f"**Medication:** {alert.get('medication_name', 'N/A')}")
                    st.write(f"**AI Summary:** {alert.get('ai_summary', 'N/A')}")
                    st.write(f"**Actions Required:** {alert.get('actions_required', 'N/A')}")
                    if alert.get('pdf_url'):
                        st.link_button("View PDF", alert['pdf_url'])
                    if alert.get('source_url'):
                        st.link_button("Source URL", alert['source_url'])

                with st.popover("Surgery Actions", icon=":material/badge:"):
                    actions = get_actions()
                    surgeries = get_surgeries()
                    profiles = get_all_profiles()

                    # Create a dictionary for quick lookup
                    surgery_dict = {s['id']: s for s in surgeries}
                    profile_dict = {p['user_id']: p for p in profiles}

                    # Filter actions for the current alert
                    filtered_actions = []
                    for action in actions:
                        if action['alert_id'] == alert['id']:
                            surgery = surgery_dict.get(action['surgery_id'])
                            if surgery:
                                pharmacist_id = surgery.get('pharmacist_id')
                                profile = profile_dict.get(pharmacist_id) if pharmacist_id else None
                                user_name = profile['full_name'] if profile else "Unknown User"
                                filtered_actions.append({
                                    'surgery_name': surgery['name'],
                                    'user_name': user_name,
                                    'action_taken': action['action_taken'],
                                    'status': action['status']
                                })

                    if filtered_actions:
                        for action in filtered_actions:
                            st.write(f"- **Surgery:** {action['surgery_name']}")
                            st.write(f"  - **Action:** {action['action_taken']}")
                            st.write(f"  - **Status:** {action['status']}")
                            st.write(f"  - **Recorded by:** {action['user_name']}")
                    else:
                        st.write("No related actions found for this alert.")

        else:
            st.info("No alerts to display.")

    elif menu_selection == "Manage Surgeries":
        manage_surgeries_page()

    elif menu_selection == "Manage Actions":
        manage_actions_page()

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
