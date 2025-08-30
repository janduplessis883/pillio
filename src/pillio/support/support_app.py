import streamlit as st
import pandas as pd

from support.support_ui import color_message_box, gradient_border_box, color_header
from support.support_supabase import (
    get_surgeries, add_surgery, update_surgery, delete_surgery,
    sign_up, sign_in, sign_out,
    get_all_users, get_all_profiles, update_user_role, delete_user,
    get_alerts, get_actions, add_action, update_action, delete_action
)


def auth_screen():

    c1,c2,c3 = st.columns([2,1.5,2])

    with c2:
        st.image("images/pillio.png")
        option = st.selectbox("Choose an action:", ["Login", "Sign Up"])


        if option == "Sign Up":
            with st.form("signup_form", clear_on_submit=True, border=False):
                name = st.text_input("Name", icon=":material/person:")
                email = st.text_input("Email", icon=":material/email:")
                password = st.text_input("Password", type="password", icon=":material/lock:")
                submitted = st.form_submit_button("Register")
                if submitted:
                    user = sign_up(email, password, name)
                    if user and user.user:
                        st.success("Registration successful! You can now log in.")
        else:
            with st.form("login_form", clear_on_submit=True, border=False):
                email = st.text_input("Email", icon=":material/email:")
                password = st.text_input("Password", type="password", icon=":material/lock:")
                submitted = st.form_submit_button("Login")
                if submitted:
                    user = sign_in(email, password)
                    if user and user.user:
                        st.session_state.user_email = user.user.email
                        st.session_state.user_name = user.user.user_metadata.get('full_name', 'Friend')
                        st.rerun()


def manage_surgeries_page():
    color_header("Manage Surgeries")

    surgeries = get_surgeries()
    if not surgeries:
        st.info("No surgeries found. Add one below.")
        df_surgeries = pd.DataFrame(columns=['id', 'name', 'location', 'contact_email'])
    else:
        df_surgeries = pd.DataFrame(surgeries)

    st.subheader("Existing Surgeries")
    st.dataframe(df_surgeries[['id', 'name', 'location', 'contact_email']], use_container_width=True)

    st.subheader("Add or Edit Surgery")

    with st.form("surgery_form", clear_on_submit=True):
        surgery_list = [s['id'] for s in surgeries] if surgeries else []
        selected_id = st.selectbox(
            "Select Surgery to Edit (or leave blank to add new)",
            options=[""] + surgery_list,
            format_func=lambda x: f"ID: {x} - {next((s['name'] for s in surgeries if s['id'] == x), '')}" if x else "Add New Surgery"
        )

        default_name = ""
        default_location = ""
        default_email = ""
        if selected_id:
            selected_surgery = next((s for s in surgeries if s['id'] == selected_id), None)
            if selected_surgery:
                default_name = selected_surgery.get('name', '')
                default_location = selected_surgery.get('location', '')
                default_email = selected_surgery.get('contact_email', '')

        name = st.text_input("Surgery Name", value=default_name)
        location = st.text_input("Location", value=default_location)
        contact_email = st.text_input("Contact Email", value=default_email)

        submitted = st.form_submit_button("Save Surgery")

        if submitted:
            if not name or not location or not contact_email:
                st.warning("Please fill out all fields.")
            else:
                if selected_id:
                    update_surgery(selected_id, name, location, contact_email)
                else:
                    add_surgery(name, location, contact_email)
                st.rerun()

    st.subheader("Delete Surgery")
    if surgeries:
        delete_id = st.selectbox(
            "Select Surgery to Delete",
            options=[""] + [s['id'] for s in surgeries],
            format_func=lambda x: f"ID: {x} - {next((s['name'] for s in surgeries if s['id'] == x), '')}" if x else "Select a surgery",
            key="delete_select"
        )
        if delete_id:
            if st.button("Delete Selected Surgery", type="primary"):
                delete_surgery(delete_id)
                st.rerun()


def manage_actions_page():
    color_header("Manage Actions")

    actions = get_actions()
    alerts = get_alerts()
    surgeries = get_surgeries()

    if not actions:
        st.info("No actions found. Add one below.")
        df_actions = pd.DataFrame(columns=['id', 'action_taken', 'notes'])
    else:
        df_actions = pd.DataFrame(actions)

    st.subheader("Existing Actions")
    st.dataframe(df_actions[['id', 'alert_id', 'surgery_id', 'action_taken', 'notes', 'status', 'recorded_by', 'recorded_date']], use_container_width=True)

    st.subheader("Add or Edit Action")

    with st.container(border=True):
        action_list = [a['id'] for a in actions] if actions else []
        selected_id = st.selectbox(
            "Select Action to Edit (or leave blank to add new)",
            options=[""] + action_list,
            format_func=lambda x: f"ID: {x} - {next((a['action_taken'] for a in actions if a['id'] == x), '')}" if x else "Add New Action"
        )

        default_action_taken = ""
        default_notes = ""
        default_status = "pending"
        default_alert_id = None
        default_surgery_id = None
        default_patients_affected = 0

        if selected_id:
            selected_action = next((a for a in actions if a['id'] == selected_id), None)
            if selected_action:
                default_action_taken = selected_action.get('action_taken', '')
                default_notes = selected_action.get('notes', '')
                default_status = selected_action.get('status', 'pending')
                default_alert_id = selected_action.get('alert_id')
                default_surgery_id = selected_action.get('surgery_id')
                default_patients_affected = selected_action.get('patients_affected', 0)

        if alerts:
            alert_options = [a['id'] for a in alerts]
            alert_index = alert_options.index(default_alert_id) if default_alert_id and default_alert_id in alert_options else 0
            alert_id = st.selectbox(
                "Select Alert",
                options=alert_options,
                format_func=lambda x: f"ID: {x} - {next((a['title'] for a in alerts if a['id'] == x), '')}",
                index=alert_index
            )
        else:
            st.warning("No alerts available. Please create an alert first.")
            alert_id = None

        if surgeries:
            surgery_options = [s['id'] for s in surgeries]
            surgery_index = surgery_options.index(default_surgery_id) if default_surgery_id and default_surgery_id in surgery_options else 0
            surgery_id = st.selectbox(
                "Select Surgery",
                options=surgery_options,
                format_func=lambda x: f"ID: {x} - {next((s['name'] for s in surgeries if s['id'] == x), '')}",
                index=surgery_index
            )
        else:
            st.warning("No surgeries available. Please create a surgery first.")
            surgery_id = None

        patients_affected = st.number_input("Patients Affected", min_value=0, value=default_patients_affected)
        action_taken = st.text_input("Action Taken", value=default_action_taken)
        notes = st.text_area("Notes", value=default_notes)
        status = st.selectbox("Status", ["pending", "in_progress", "completed"], index=["pending", "in_progress", "completed"].index(default_status))

        if st.button("Save Action"):
            if not action_taken or not alert_id or not surgery_id:
                st.warning("Please fill out all fields and ensure alerts and surgeries are available.")
            else:
                if 'user_id' in st.session_state and st.session_state.user_id:
                    recorded_by = st.session_state.user_id
                    if selected_id:
                        update_action(selected_id, alert_id, surgery_id, patients_affected, action_taken, notes, status, recorded_by)
                    else:
                        add_action(alert_id, surgery_id, patients_affected, action_taken, notes, status, recorded_by)
                    st.rerun()
                else:
                    st.error("Could not identify user. Please log in again.")

    st.subheader("Delete Action")
    if actions:
        delete_id = st.selectbox(
            "Select Action to Delete",
            options=[""] + [a['id'] for a in actions],
            format_func=lambda x: f"ID: {x} - {next((a['action_taken'] for a in actions if a['id'] == x), '')}" if x else "Select an action",
            key="delete_action_select"
        )
        if delete_id:
            if st.button("Delete Selected Action", type="primary"):
                delete_action(delete_id)
                st.rerun()


def manage_users_page():
    color_header("Manage Users")

    profiles = get_all_profiles()
    if profiles:
        df_profiles = pd.DataFrame(profiles)

        # Get all users to map emails
        users = get_all_users()
        user_email_map = {user.id: user.email for user in users}
        df_profiles['email'] = df_profiles['user_id'].map(user_email_map)

        st.subheader("User Roles")
        st.dataframe(df_profiles[['email', 'full_name', 'role']], use_container_width=True)

        st.subheader("Update User Role")

        with st.form("update_role_form", clear_on_submit=True):
            user_to_update = st.selectbox(
                "Select User",
                options=df_profiles['user_id'],
                format_func=lambda x: df_profiles[df_profiles['user_id'] == x]['email'].iloc[0]
            )

            new_role = st.selectbox(
                "Select New Role",
                options=['pharmacist', 'practice_manager', 'doctor', 'administrator']
            )

            submitted = st.form_submit_button("Update Role")
            if submitted:
                update_user_role(user_to_update, new_role)
                st.rerun()

        st.subheader("Delete User")
        user_to_delete = st.selectbox(
            "Select User to Delete",
            options=[""] + list(df_profiles['user_id']),
            format_func=lambda x: df_profiles[df_profiles['user_id'] == x]['email'].iloc[0] if x else "Select a user",
            key="delete_user_select"
        )
        if user_to_delete:
            if st.button("Delete Selected User", type="primary"):
                delete_user(user_to_delete)
                st.rerun()
    else:
        st.info("No user profiles found.")


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
