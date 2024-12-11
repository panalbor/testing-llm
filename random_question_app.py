import streamlit as st
import random
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define scopes for Google Sheets API
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load service account credentials
SERVICE_ACCOUNT_FILE = "credentials.json"  # Replace with your JSON file path
credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)

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


# Contexts
CONTEXTS = [
    """Overview:
Alexandra, a Partner Marketing Specialist at a technology company, was facing the challenge of creating a community for SUSE partners and motivating them to complete trainings and certifications. To address this challenge, Alexandra turned to Captivate Collective, a premiere provider of customer programs strategy, program operationalization, and educational offerings that help organizations drive business impact by identifying, engaging, and collaborating with their customers.
Engaging Captivate Collective:
Alexandra decided to leverage Captivate Collective's consulting services to launch the SUSE Champions program. This decision was driven by the need to create a customer advocacy program that would motivate and activate customers across various stages of their journey, from acquisition to advocacy.
The primary goals of the SUSE Champions program were to create a sense of community among SUSE partners, drive engagement, and motivate partners to complete trainings and certifications. To achieve these goals, Captivate Collective provided Alexandra with a variety of strategies that focused on the entire customer journey, helping to build stronger brand affinity and loyalty.""",
    """
Jia, the Director of Business Development for a technology company, began using Callbox's services in 2019. She was seeking a solution to help her team cast a larger net and reach a wider audience, ultimately aiming to improve their lead generation and prospecting efforts. The deciding factor for Jia was the combination of Callbox's expertise in lead generation and the cost-effective nature of their services.
From the very beginning, Jia found the Callbox team to be prompt, flexible, and professional. Their project management style was impressive, with a strong emphasis on the feedback process, flexibility, and timeliness. The Callbox team was always available to answer any questions or concerns that Jia had throughout the project.
One of the most impressive aspects of Callbox, as noted by Jia, was their ability to customize their own script. This allowed Jia and her team to be fully hands-on with Callbox, ensuring that the messaging was tailored specifically to the needs of their company and target audience.
    """,
    """Dan, a Sales Manager in the diagnostic imaging industry, has been using Callbox's services since 2023. He has found that the company's expertise in lead generation and marketing solutions has significantly impacted his team's sales process and overall revenue. With a keen understanding of the unique challenges faced by the diagnostic imaging industry, Callbox has proven to be a valuable partner for Dan and his team.

Engaging Callbox

Dan was initially drawn to Callbox's services due to their excellent customer service, flexibility, and willingness to make adjustments as needed. These factors played a crucial role in his decision to engage Callbox for their lead generation and marketing needs.

Project Management Style

Callbox's project management style has been a significant factor in their successful collaboration with Dan and his team. The Callbox team is highly accessible, responsive, and takes the time to understand the unique nature of the diagnostic imaging marketplace. They are open to feedback and can course-correct at any time, ensuring that the project stays on track and delivers the desired results.""",
    """Bianca, a Consultant Extraordinaire at an agency in the industry, sought to address several pressing challenges her organization faced. These included incorporating strategic direction, minimizing ad hoc requests, and growing a portfolio of programs. As a result, Bianca turned to Captivate Collective for assistance, ultimately deciding to partner with them based on their experience and perspective.

Captivate Collective, a premiere provider of customer programs strategy, program operationalization, and educational offerings, is known for helping organizations drive business impact by identifying, engaging, and collaborating with their customers. Their strategies inspire and mobilize customers across their entire journey, intentionally building brand affinity and loyalty, from acquisition to advocacy.

To help Bianca's organization, Captivate Collective provided coaching and consulting services aimed at upleveling the team's knowledge and developing a robust strategy for their portfolio. The result was a clearly mapped out advocate journey for customers that became an integral part of their day-to-day experience working with the agency.

Bianca has seen significant benefits from working with Captivate Collective, including a huge time to value and validation from her organization's leadership team. The agency's customer-centric approach and trusted coaching have truly elevated their advocacy strategy, bringing a wealth of industry perspective to the table and helping them identify and engage with customers in a meaningful way.""",
    """Mark, a Sr Director of Services Support and Strategy at a consulting company, faced significant challenges in managing the company's IT infrastructure and business applications. Before implementing Faddom's Agentless Application Dependency Mapping Tool, Mark and his team had no visibility or insight into how their applications communicated with each other. This lack of understanding posed risks when making changes to the infrastructure, potentially affecting business applications and revenue generation.

The deployment and implementation of Faddom's solution proved to be a game-changer for Mark and his team. The ease of installation in their VMware environment allowed them to quickly access the platform's features and start reaping the benefits. As a result, the consulting company experienced three significant advantages after implementing Faddom’s solution:

1. Network Topology View: Faddom's platform provided a comprehensive visualization of the company's on-premise and cloud infrastructure. This real-time view of the network topology enabled Mark and his team to make informed decisions when modifying the IT infrastructure, ensuring that business applications continued to function effectively and generate revenue.

2. Real-Time Communication Status: Faddom's tool allowed the IT team to monitor the communication status of their applications in real-time. This ability to track application interactions helped identify potential bottlenecks or issues before they escalated, ensuring smoother operation and increased efficiency.

3. Subnet Mappings: The platform's subnet mapping feature proved invaluable for understanding the dependencies between servers and applications. By providing a clear view of these relationships, Faddom's solution enabled Mark and his team to make informed decisions when implementing changes, minimizing the risk of disruptions to business applications.""",
]

FIELDS = [
    "Suggest the question",
    "Answer to the suggested question",
    "Is the question corresponds to the context?",
    "Is there unambiguous answer?",
    "Explain why did you suggest this question"
]

# Define your questions and associated fields
QUESTIONS = [
    {
        "context": x,
        "fields": FIELDS
    }
    for x in CONTEXTS
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
st.title("Suggest question")
st.subheader("The context is given. Please, suggest the question and fill other fields below")

# Display the random context
st.write(f"**Context:** {selected_context['context']}")

# Form to collect answers
with st.form(key="response_form"):

    responses = {}
    for field in selected_context["fields"]:
        responses[field] = st.text_input(f"{field}:")
    
    # Submit button
    submit_button = st.form_submit_button(label="Submit")

# Handle form submission
if submit_button:
    # # Save responses to CSV
    data = {"Context": selected_context["context"], **responses}
    
    # # Append to CSV if it exists, else create a new file
    # if os.path.exists(FILE_NAME):
    #     df.to_csv(FILE_NAME, mode="a", header=False, index=False)
    # else:
    #     df.to_csv(FILE_NAME, index=False)
    
    # data_to_save = [selected_context["context"], responses]
    save_to_google_sheet(list(data.values()))
    # st.success("Response saved to Google Sheet!")

    st.success("Thank you for your response! Your data has been saved.")
    st.write("Here is what you submitted:")
    for field, response in responses.items():
        st.write(f"- **{field}:** {response}")

# Button to go to a new context
if st.button("Go to the other context"):
    get_new_context()
