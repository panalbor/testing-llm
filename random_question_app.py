import streamlit as st
import random
import pandas as pd
import os
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# Define scopes for Google Sheets API
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load service account credentials from Streamlit Secrets
credentials_json = st.secrets["GCP_CREDENTIALS"]  # Loaded as a dictionary
credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(credentials_json), SCOPES)

# Authorize and connect to Google Sheets
gc = gspread.authorize(credentials)

# Open the spreadsheet by its ID or URL
SPREADSHEET_ID = "1G7dBnErkMcsqmnUAMdjW6aN8EQFc4wyaaGDa3tTcXpw"  # Replace with your spreadsheet ID
sheet = gc.open_by_key(SPREADSHEET_ID).sheet1  # Access the first sheet

# all_responses = sheet.get_all_records()

# Function to write responses to the Google Sheet
def save_to_google_sheet(data):
    # Append the data as a new row
    sheet.append_row(data)

contexts_df = pd.read_csv("contexts.csv")

FIELDS = [
    "Suggest a question that can be related to the context",
    "Indicate the correct answer",
    "Is the proposed question about the content of the text, its form, or something else?",
    "Does the context contain the answer to the suggested question?",
    "Explain the reason of the question and your answers"
]

# Define your questions and associated fields
QUESTIONS = [
    {
        "context_id": row["context_id"],
        "context": row["context"],
        "fields": FIELDS
    }
    for _, row in contexts_df.iterrows()
]

# File to store responses
FILE_NAME = "responses.csv"

# Initialize session state to store the selected context
if "selected_context" not in st.session_state:
    st.session_state["selected_context"] = random.choice(QUESTIONS)

# Function to select a new random context
def get_new_context():
    st.session_state["selected_context"] = random.choice(QUESTIONS)
    # Simulate a page reload by setting query params
    st.rerun()

# Get the current selected context
selected_context = st.session_state["selected_context"]

# Streamlit app layout
st.title("Task: suggest a question")
st.subheader("Instruction: For the given context suggest the question.")

# Display the random context
st.write(f"**Context:** {selected_context['context']}")

# Form to collect answers
with st.form(key="response_form"):

    responses = {}
    for field in FIELDS:
        
        responses[field] = st.text_input(f"{field}")
    
    # Submit button
    submit_button = st.form_submit_button(label="Submit")

# Handle form submission
if submit_button:
    # # Save responses to CSV
    data = {"Context": selected_context["context_id"], **responses}
    
    save_to_google_sheet(list(data.values()))
    # st.success("Response saved to Google Sheet!")

    st.success("Thank you for your response! Your data has been saved.\n You can suggest another question for this context, or jump to another by clicking on the button below")
    st.write("Here is what you submitted:")
    for field, response in responses.items():
        st.write(f"- **{field}:** {response}")

# Button to go to a new context
if st.button("Go to the other context"):
    get_new_context()
