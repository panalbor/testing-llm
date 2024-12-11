import json
import streamlit as st

# Access the secret
credentials_json = st.secrets["GCP_CREDENTIALS"]

# Parse JSON
credentials = json.loads(credentials_json)
st.write(credentials)

