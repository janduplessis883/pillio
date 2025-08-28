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
        st.toast(color_message_box("Task added successfully!", icond=":material/check:"))
        time.sleep(3)
    except Exception as e:
        color_message_box(f"Error fetching todos: {e}")
        return []

def add_todo(task):
    try:
        supabase.table('todos').insert({'task': task}).execute()
        st.toast(color_message_box("Task added successfully!", icond=":material/check:"))
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
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return user
    except Exception as e:
        st.error(f"Login failed: {e}")

def sign_out():
    try:
        supabase.auth.sign_out()
        st.session_state.user_email = None

        st.session_state.user_name = None
        st.success("You have been logged out.")
        st.rerun()
    except Exception as e:
        st.error(f"Logout failed: {e}")
