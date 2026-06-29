import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def save_response(responses, name, phone, email, circle):
    try:
        # Get credentials from Streamlit secrets
        client_id = st.secrets["client_id"]
        client_secret = st.secrets["client_secret"]
        
        # Create credentials manually
        credentials_dict = {
            "type": "oauth2",
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
        
        # Authenticate with Google Sheets
        credentials = Credentials.from_authorized_user_info(credentials_dict, scopes=SCOPES)
        client = gspread.authorize(credentials)
        
        # Open the Google Sheet by name
        sheet = client.open('Thrive with Morella Surveys').sheet1
        
        # Prepare the row data
        row = [str(datetime.now()), circle] + list(responses.values()) + [name, phone, email]
        sheet.append_row(row)
        
    except Exception as e:
        st.error(f"Error saving response: {str(e)}")
