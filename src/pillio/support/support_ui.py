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

def alert_card(title: str, issue_date: str, source: str, alert_reference: str):
    html_code = f"""
    <div style="
        position: relative;
        background: white;
        color: #4a3735;
        padding: 12px 20px;
        border-radius: 9px;
        font-family: 'Segoe UI', Roboto, sans-serif;
        font-size: 14px;
        border: 1px solid transparent;
        background-image: linear-gradient(135deg, white, #f2f2f0),
                          linear-gradient(135deg, #dc4c87, #ef9035);
        background-origin: border-box;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        background-clip: padding-box, border-box;">

        <!-- Title -->
        <div style="font-size: 18px; font-weight: 600; color: #4a3735; margin-bottom: 10px;">
            {title}
        </div>

        <!-- Horizontal Meta Info -->
        <div style="display: flex; gap: 20px; font-size: 14px; color: #4a3735;">
            <div>Issue Date: <strong>{issue_date}</strong></div>
            <div>Reference: <strong>{alert_reference}</strong></div>
            <div>Source: <strong>{source}</strong></div>
        </div>
    </div>
    """
    st.html(html_code)
