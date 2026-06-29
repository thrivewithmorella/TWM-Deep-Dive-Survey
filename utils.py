import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st
import json

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

def save_response(responses, name, phone, email, circle):
    try:
        # Get service account credentials from Streamlit secrets
        service_account_info = st.secrets["google_service_account"]
        
        # Create credentials from the service account info with correct scopes
        credentials = Credentials.from_service_account_info(
            service_account_info,
            scopes=SCOPES
        )
        
        # Authorize with gspread
        client = gspread.authorize(credentials)
        
        # Open the Google Sheet by name
        sheet = client.open('Thrive with Morella Surveys').sheet1
        
        # Prepare the row data
        row = [str(datetime.now()), circle] + list(responses.values()) + [name, phone, email]
        sheet.append_row(row)
        
    except Exception as e:
        st.error(f"Error saving response: {str(e)}")
