import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st
import json

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

def save_response(responses, name, phone, email, circle, sheet_name):
    try:
        service_account_info = st.secrets["google_service_account"]
        credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
        client = gspread.authorize(credentials)
        
        # Open the specified sheet
        sheet = client.open(sheet_name).sheet1
        
        # Build the row
        row = [str(datetime.now()), circle]
        
        # Question 1: Challenge Categories
        q1_selected = responses.get(0, {}).get("selected", [])
        q1_options = [
            "Relationship challenges of any kind (with spouses, parents, children, friends, or coworkers) - including communication and boundary challenges.",
            "Time management and life balance challenges - including difficulty prioritizing yourself.",
            "Difficulty with self-esteem and confidence.",
            "Physical and/or emotional health challenges - including chronic health issues, and/or difficulty managing anxiety, anger, stress, and irritation.",
            "Dealing with the effects of trauma",
            "Challenges in your career or your finances",
            "Something else"
        ]
        q1_categories = [q1_options[i] for i in q1_selected]
        row.append("; ".join(q1_categories))
        
        # Question 1: Other text (if "Something else" was selected)
        q1_other = responses.get(0, {}).get("other_text", "")
        row.append(q1_other)
        
        # Question 2: Feelings
        q2_selected = responses.get(1, {}).get("selected", [])
        q2_options = [
            "Burnt out. Exhausted.",
            "Overwhelmed.",
            "Frozen.",
            "Disconnected from myself and/or from everyone else",
            "Irritated, angry or even irate",
            "Anxious, scared, or even panicked",
            "Stressed",
            "Tired and wired",
            "Lonely",
            "Something else"
        ]
        q2_feelings = [q2_options[i] for i in q2_selected]
        row.append("; ".join(q2_feelings))
        
        # Question 2: Other text (if "Something else" was selected)
        q2_other = responses.get(1, {}).get("other_text", "")
        row.append(q2_other)
        
        # Contact information
        row.extend([name, phone, email])
        
        # Append the row to the sheet
        sheet.append_row(row)
        
    except Exception as e:
        st.error(f"Error saving response: {str(e)}")
