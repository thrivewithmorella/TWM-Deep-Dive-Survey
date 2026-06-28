import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime
import streamlit as st

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def save_response(responses, name, phone, email, circle):
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
    credentials = flow.run_local_server(port=0)
    client = gspread.authorize(credentials)
    
    # Open the Google Sheet by name
    sheet = client.open('Thrive with Morella Surveys').sheet1
    
    row = [str(datetime.now()), circle] + list(responses.values()) + [name, phone, email]
    sheet.append_row(row)
