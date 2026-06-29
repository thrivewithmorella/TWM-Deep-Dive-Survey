import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st
import json

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

def save_response(responses, name, phone, email, circle):
    try:
        st.write("DEBUG: Starting save_response function")
        
        # Get service account credentials from Streamlit secrets
        service_account_info = st.secrets["google_service_account"]
        st.write("DEBUG: Got service account credentials")
        
        # Create credentials from the service account info with correct scopes
        credentials = Credentials.from_service_account_info(
            service_account_info,
            scopes=SCOPES
        )
        st.write("DEBUG: Created credentials")
        
        # Authorize with gspread
        client = gspread.authorize(credentials)
        st.write("DEBUG: Authorized with gspread")
        
        # Open the Google Sheet by name
        sheet = client.open('Thrive with Morella Surveys').sheet1
        st.write("DEBUG: Opened Google Sheet")
        
        # Prepare the row data
        row = [str(datetime.now()), circle]
        row.append(responses.get(0, ""))
        row.append(responses.get(1, ""))
        row.append(responses.get(2, ""))
        row.append(responses.get(3, ""))
        row.extend([name, phone, email])
        
        st.write(f"DEBUG: Row data prepared: {row}")
        
        sheet.append_row(row)
        st.write("DEBUG: Row appended to sheet successfully!")
        
    except Exception as e:
        st.error(f"Error saving response: {str(e)}")
        st.write(f"DEBUG: Full error: {e}")
