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
        q1_data = responses.get(0, {})
        if isinstance(q1_data, dict):
            q1_selected = q1_data.get("selected", [])
            q1_options = [
                "Relationship challenges of any kind (with spouses, parents, children, friends, or coworkers) - including communication and boundary challenges.",
                "Time management and life balance challenges - including difficulty prioritizing yourself.",
                "Difficulty with self-esteem and confidence.",
                "Physical and/or emotional health challenges - including chronic health issues, and/or difficulty managing anxiety, anger, stress, and irritation.",
                "Dealing with the effects of trauma",
                "Challenges in your career or your finances",
                "Something else"
            ]
            q1_categories = [q1_options[i] for i in q1_selected if i < len(q1_options)]
            row.append("; ".join(q1_categories))
            row.append(q1_data.get("other_text", ""))
        else:
            row.append("")
            row.append("")
        
        # Question 2: Feelings
        q2_data = responses.get(1, {})
        if isinstance(q2_data, dict):
            q2_selected = q2_data.get("selected", [])
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
            q2_feelings = [q2_options[i] for i in q2_selected if i < len(q2_options)]
            row.append("; ".join(q2_feelings))
            row.append(q2_data.get("other_text", ""))
        else:
            row.append("")
            row.append("")
        
        # Question 3: Challenge Details (open-ended, only for Emerging and Active)
        q3_data = responses.get(2, "")
        if isinstance(q3_data, str):
            row.append(q3_data)
        else:
            row.append("")
        
        # Contact information
        row.extend([name, phone, email])
        
        # Append the row to the sheet
        sheet.append_row(row)
        
    except Exception as e:
        st.error(f"Error saving response: {str(e)}")
