import streamlit as st

# UI Configuation
def color_message_box(message: str):
    html_code = f"""
    <div style="
        background: linear-gradient(135deg, #dc4c87, #ef9035);
        color: white;
        padding: 9px 20px;
        border-radius: 6px;
        font-family: Arial, sans-serif;
        font-size: 14px;">
      {message}
    </div>
    """
    st.html(html_code)

def gradient_border_box(message: str):
    html_code = f"""
    <div style="
        position: relative;
        background: white;
        color: #4a3735;
        padding: 8px 20px;
        border-radius: 9px;
        font-family: Arial, sans-serif;
        font-size: 14px;
        border: 1px solid transparent;
        background-image: linear-gradient(white, white),
                          linear-gradient(135deg, #dc4c87, #ef9035);
        background-origin: border-box;
        background-clip: padding-box, border-box;">
      {message}
    </div>
    """
    st.html(html_code)

def color_header(message: str):
    html_code = f"""
    <div style="
        background: linear-gradient(135deg, #dc4c87, #ef9035);
        color: white;
        padding: 7px 20px;
        border-radius: 10px;
        font-family: Arial, sans-serif;
        font-size: 24px;
        font-weight: 700;">
      {message}
    </div>
    """
    st.html(html_code)
