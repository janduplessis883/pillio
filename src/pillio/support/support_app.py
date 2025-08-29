import streamlit as st
import pandas as pd

from support.support_ui import color_message_box, gradient_border_box, color_header
from support.support_supabase import get_surgeries, add_surgery, update_surgery, delete_surgery, sign_up, sign_in, sign_out, get_all_users, get_all_profiles, update_user_role


def auth_screen():
    st.image("images/pillio.png")

    c1,c2,c3 = st.columns([2,1.5,2])

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

        user_to_update = st.selectbox(
            "Select User",
            options=df_profiles['user_id'],
            format_func=lambda x: df_profiles[df_profiles['user_id'] == x]['email'].iloc[0]
        )

        new_role = st.selectbox(
            "Select New Role",
            options=['pharmacist', 'practice_manager', 'doctor', 'administrator']
        )

        if st.button("Update Role"):
            update_user_role(user_to_update, new_role)
            st.rerun()
    else:
        st.info("No user profiles found.")
