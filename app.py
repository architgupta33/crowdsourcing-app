# import streamlit as st
# import gspread
# import os
# import json
# from oauth2client.service_account import ServiceAccountCredentials
# from huggingface_hub import InferenceClient

# # Load Hugging Face API token from environment variable
# # HF_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
# # if not HF_API_TOKEN:
# #     st.error("Hugging Face API token is missing. Set HUGGINGFACE_API_TOKEN in your environment.")
# #     st.stop()

# # Load API token from secrets
# HF_API_TOKEN = st.secrets["HUGGINGFACE_API_TOKEN"]

# # api = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.1", token=HF_API_TOKEN)  # Add authentication token)
# api = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=HF_API_TOKEN)  # Add authentication token)

# # Load Google Cloud credentials from environment variable
# google_credentials_json = os.getenv("GOOGLE_CREDENTIALS")
# if not google_credentials_json:
#     st.error("Google Cloud credentials are missing. Set GOOGLE_CREDENTIALS in your environment.")
#     st.stop()

# # Parse the JSON credentials from environment variable
# try:
#     google_credentials = json.loads(google_credentials_json)
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = ServiceAccountCredentials.from_json_keyfile_dict(google_credentials, scope)
#     client = gspread.authorize(creds)
# except Exception as e:
#     st.error(f"Failed to authenticate with Google Sheets: {e}")
#     st.stop()

# # Access Google Sheets
# try:
#     sheet_vote = client.open("Crowdsourcing-app").get_worksheet(0)
#     sheet_feedback = client.open("Crowdsourcing-app").get_worksheet(1)
# except Exception as e:
#     st.error(f"Error accessing Google Sheets: {e}")
#     st.stop()

# # Streamlit App Interface
# st.title("Crowdsourced Feedback App")

# # Image Upload Section
# st.subheader("Upload Two Competing Images for Voting")
# uploaded_images = st.file_uploader("Upload two images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

# if uploaded_images and len(uploaded_images) == 2:
#     st.image(uploaded_images, caption=["Option 1", "Option 2"], width=300)

#     # User Dilemma Post
#     post = st.text_area("Describe your dilemma (e.g., which outfit looks better?)")
#     if st.button("Post Dilemma"):
#         if post:
#             sheet_feedback.append_row([post, "Pending"])
#             st.success("Your dilemma has been posted!")
#             st.session_state.dilemma_posted = True  # Set the state to True after posting
#         else:
#             st.warning("Please provide a dilemma description.")
    
#     # Hide upload box
#     st.markdown("<style>.stFileUploader {display: none;}</style>", unsafe_allow_html=True)

#     # Check if dilemma has been posted
#     if st.session_state.get('dilemma_posted', False):
#         # Voting Buttons
#         if st.button("Vote for Option 1"):
#             sheet_vote.append_row(["Option 1", "1"])
#             st.success("You voted for Option 1!")

#         if st.button("Vote for Option 2"):
#             sheet_vote.append_row(["Option 2", "1"])
#             st.success("You voted for Option 2!")

#         # Fetch and Display Votes
#         st.subheader("Community Votes")
#         vote = sheet_vote.col_values(1)
#         feedback = sheet_feedback.col_values(1)

#         # Summarize Feedback with Llama 3.1
#         if len(vote) > 0:
#             st.subheader("Feedback Summary")
#             # Define input prompt
#             prompt_vote = "You are a count checker. There are 2 photo options a user can place a vote for. Summarize the count of votes: " + str(vote)

#             # Call the API
#             response = api.chat_completion(messages=[{"role": "user", "content": prompt_vote}])
            
#             # Extract the value from the 'content' key in the response
#             if response and 'choices' in response and len(response['choices']) > 0:
#                 content = response['choices'][0]['message']['content']
#                 st.write(content)
#             else:
#                 st.error("Failed to fetch a valid response from the API.")


import streamlit as st
import gspread
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from oauth2client.service_account import ServiceAccountCredentials
from huggingface_hub import InferenceClient

# Load Hugging Face API token from secrets
HF_API_TOKEN = st.secrets["HUGGINGFACE_API_TOKEN"]
api = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=HF_API_TOKEN)

# Load Google Cloud credentials
google_credentials_json = os.getenv("GOOGLE_CREDENTIALS")
if not google_credentials_json:
    st.error("Google Cloud credentials are missing. Set GOOGLE_CREDENTIALS in your environment.")
    st.stop()

# Authenticate Google Sheets
try:
    google_credentials = json.loads(google_credentials_json)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(google_credentials, scope)
    client = gspread.authorize(creds)
except Exception as e:
    st.error(f"Failed to authenticate with Google Sheets: {e}")
    st.stop()

# Access Google Sheets
try:
    sheet_vote = client.open("Crowdsourcing-app").get_worksheet(0)
    sheet_feedback = client.open("Crowdsourcing-app").get_worksheet(1)
except Exception as e:
    st.error(f"Error accessing Google Sheets: {e}")
    st.stop()

# Streamlit App Interface
st.title("Crowdsourced Feedback App")

# Image Upload Section
st.subheader("Upload Two Competing Images for Voting")
uploaded_images = st.file_uploader("Upload two images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_images and len(uploaded_images) == 2:
    st.image(uploaded_images, caption=["Option 1", "Option 2"], width=300)

    # User Dilemma Post
    post = st.text_area("Describe your dilemma (e.g., which outfit looks better?)")
    if st.button("Post Dilemma"):
        if post:
            sheet_feedback.append_row([post, "Pending"])
            st.success("Your dilemma has been posted!")
            st.session_state.dilemma_posted = True  # Set the state to True after posting
        else:
            st.warning("Please provide a dilemma description.")

    # Hide upload box
    st.markdown("<style>.stFileUploader {display: none;}</style>", unsafe_allow_html=True)

    # Check if dilemma has been posted
    if st.session_state.get('dilemma_posted', False):
        # Voting Buttons
        if st.button("Vote for Option 1"):
            sheet_vote.append_row(["Option 1", "1"])
            st.success("You voted for Option 1!")

        if st.button("Vote for Option 2"):
            sheet_vote.append_row(["Option 2", "1"])
            st.success("You voted for Option 2!")

# Function to fetch votes
@st.cache_data(ttl=10)  # Cache data for 10 seconds
def get_votes():
    return sheet_vote.col_values(1)

# Refresh Button
if st.button("Refresh Votes"):
    st.cache_data.clear()  # Clear cache to fetch fresh votes

# Fetch updated votes
votes = get_votes()

# Display total votes
st.write(f"Total Votes: {len(votes)}")

# Vote Count
vote_counts = {"Option 1": votes.count("Option 1"), "Option 2": votes.count("Option 2")}

# Convert to DataFrame
df = pd.DataFrame(list(vote_counts.items()), columns=["Option", "Votes"])

# Plot Vote Results
st.subheader("Live Voting Results")
fig, ax = plt.subplots()
sns.barplot(x="Option", y="Votes", data=df, ax=ax, palette=["#1f77b4", "#ff7f0e"])
ax.set_title("Live Voting Results")
ax.set_ylabel("Number of Votes")
st.pyplot(fig)

# Summarize Feedback using Hugging Face API
if len(votes) > 0:
    st.subheader("Feedback Summary")
    
    # Define input prompt
    prompt_vote = "You are a count checker. There are 2 photo options a user can place a vote for. Summarize the count of votes: " + str(votes)

    # Call the API
    response = api.chat_completion(messages=[{"role": "user", "content": prompt_vote}])
    
    # Extract and display summary
    if response and 'choices' in response and len(response['choices']) > 0:
        content = response['choices'][0]['message']['content']
        st.write(content)
    else:
        st.error("Failed to fetch a valid response from the API.")
