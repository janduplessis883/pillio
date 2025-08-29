import streamlit as st
from supabase import create_client, Client
import time

from support.support_ui import color_message_box, gradient_border_box



url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

def get_todos():
    try:
        response = supabase.table('todos').select('*').execute()
        return response.data
    except Exception as e:
        color_message_box(f"Error fetching todos: {e}")
        return []

def add_todo(task):
    try:
        supabase.table('todos').insert({'task': task}).execute()
        st.toast("Task added successfully!", icon=":material/check:")
        time.sleep(1)
    except Exception as e:
        color_message_box(f"Error adding todo: {e}")

def delete_todo(task_id):
    try:
        supabase.table('todos').delete().eq('id', task_id).execute()
        st.toast("Task deleted successfully!", icon=":material/delete:")
        time.sleep(1)
    except Exception as e:
        color_message_box(f"Error deleting todo: {e}")

def update_todo(task_id, new_task):
    try:
        supabase.table('todos').update({'task': new_task}).eq('id', task_id).execute()
        st.toast("Task updated successfully!", icon=":material/edit:")
        time.sleep(1)  # Brief pause to ensure update is processed
    except Exception as e:
        color_message_box(f"Error updating todo: {e}")

def all_todos():
    try:
        response = supabase.table('todos').select('*').execute()
        return response.data
    except Exception as e:
        color_message_box(f"Error fetching all todos: {e}")
        return []

def get_alerts():
    try:
        response = supabase.table('alerts').select('*').execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching alerts: {e}")
        return []

def get_surgeries():
    try:
        response = supabase.table('surgeries').select('*').execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching surgeries: {e}")
        return []

def get_actions():
    try:
        response = supabase.table('actions').select('*').execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching actions: {e}")
        return []

def add_surgery(name, location, contact_email):
    try:
        supabase.table('surgeries').insert({
            'name': name,
            'location': location,
            'contact_email': contact_email
        }).execute()
        st.toast("Surgery added successfully!", icon="✅")
        time.sleep(1)
    except Exception as e:
        st.error(f"Error adding surgery: {e}")

def update_surgery(surgery_id, name, location, contact_email):
    try:
        supabase.table('surgeries').update({
            'name': name,
            'location': location,
            'contact_email': contact_email
        }).eq('id', surgery_id).execute()
        st.toast("Surgery updated successfully!", icon="🔄")
        time.sleep(1)
    except Exception as e:
        st.error(f"Error updating surgery: {e}")

def delete_surgery(surgery_id):
    try:
        supabase.table('surgeries').delete().eq('id', surgery_id).execute()
        st.toast("Surgery deleted successfully!", icon="🗑️")
        time.sleep(1)
    except Exception as e:
        st.error(f"Error deleting surgery: {e}")

def get_all_users():
    try:
        service_key: str = st.secrets["SUPABASE_SERVICE_KEY"]
        supabase_admin = create_client(url, service_key)
        response = supabase_admin.auth.admin.list_users()
        return response
    except Exception as e:
        st.error(f"Error fetching users: {e}")
        return []

def get_user_profile(user_id):
    try:
        return supabase.table('profiles').select('*').eq('user_id', user_id).single().execute()
    except Exception as e:
        # This might fail if the profile doesn't exist yet, so we don't show an error
        return None

def get_all_profiles():
    try:
        return supabase.table('profiles').select('*').execute().data
    except Exception as e:
        st.error(f"Error fetching profiles: {e}")
        return []

def update_user_role(user_id, role):
    try:
        service_key: str = st.secrets["SUPABASE_SERVICE_KEY"]
        supabase_admin = create_client(url, service_key)
        supabase_admin.table('profiles').update({'role': role}).eq('user_id', user_id).execute()
        st.toast(f"User role updated to {role}", icon="🔄")
    except Exception as e:
        st.error(f"Error updating user role: {e}")


# Supabase Authentication



def sign_up(email, password, name):
    try:
        user = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "full_name": name
                }
            }
        })
        return user
    except Exception as e:
        st.error(f"Registration failed: {e}")

def sign_in(email, password):
    try:
        user_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if user_response.user:
            # Fetch the user's profile to get their role
            profile_response = get_user_profile(user_response.user.id)
            if profile_response and profile_response.data:
                st.session_state.user_role = profile_response.data.get('role')
        return user_response
    except Exception as e:
        st.error(f"Login failed: {e}")

def sign_out():
    try:
        supabase.auth.sign_out()
        st.session_state.user_email = None
        st.session_state.user_name = None
        st.session_state.user_role = None
        st.success("You have been logged out.")
        st.rerun()
    except Exception as e:
        st.error(f"Logout failed: {e}")
