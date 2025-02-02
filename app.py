# import streamlit as st
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import openai

# # Set up OpenAI API key
# openai.api_key = 'your-openai-api-key'

# # Google Sheets authentication
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
# client = gspread.authorize(creds)

# # Open the Google Sheets document
# sheet = client.open("CrowdsourcedFeedbackApp").sheet1

# # Streamlit App Interface
# st.title("Crowdsourced Feedback App")

# # User post dilemma
# post = st.text_area("Describe your dilemma here (e.g., which outfit looks better?)")
# if st.button("Post"):
#     if post:
#         # Store post in Google Sheets
#         sheet.append_row([post, "Pending", "Pending", "Pending"])
#         st.write("Your dilemma has been posted! Feedback will be gathered soon.")
#     else:
#         st.write("Please provide a dilemma description.")

# # Display feedback from the community
# st.write("Feedback from the community:")
# feedback = sheet.col_values(1)  # Get all posts from column 1 (Post column)
# st.write(feedback)

# # Summarize feedback using OpenAI
# if len(feedback) > 1:
#     st.write("Feedback Summary:")
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=f"Summarize this feedback: {feedback}",
#         max_tokens=100
#     )
#     st.write(response.choices[0].text.strip())





# import streamlit as st
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from transformers import pipeline

# # Load the Hugging Face summarization pipeline (this will automatically use the API key if set in the environment)
# # summarizer = pipeline("summarization", model="meta-llama/Llama-3.1-8B")

# summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)


# # Google Sheets authentication
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
# client = gspread.authorize(creds)

# # Open the Google Sheets document
# sheet = client.open("Crowdsourcing-app").sheet1

# # Streamlit App Interface
# st.title("Crowdsourced Feedback App")

# # User post dilemma
# post = st.text_area("Describe your dilemma here (e.g., which outfit looks better?)")
# if st.button("Post"):
#     if post:
#         # Store post in Google Sheets
#         sheet.append_row([post, "Pending", "Pending", "Pending"])
#         st.write("Your dilemma has been posted! Feedback will be gathered soon.")
#     else:
#         st.write("Please provide a dilemma description.")

# # Display feedback from the community
# st.write("Feedback from the community:")
# feedback = sheet.col_values(1)  # Get all posts from column 1 (Post column)
# st.write(feedback)

# # Summarize feedback using Hugging Face's Llama 3.1
# if len(feedback) > 1:
#     st.write("Feedback Summary:")

#     # Combine all feedback for summarization
#     combined_feedback = " ".join(feedback)

#     try:
#         # Use the Hugging Face summarization model
#         summarized = summarizer(combined_feedback, max_length=150, min_length=50, do_sample=False)
#         st.write(summarized[0]['summary_text'])
#     except Exception as e:
#         st.write(f"Error while summarizing feedback: {e}")




# import streamlit as st
# import gspread
# import os
# from oauth2client.service_account import ServiceAccountCredentials
# from huggingface_hub import InferenceClient

# # Load Hugging Face API token from environment variable
# # HF_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
# # if not HF_API_TOKEN:
# #     st.error("Hugging Face API token is missing. Set HUGGINGFACE_API_TOKEN in your environment.")
# #     st.stop()

# api = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta")

# # Google Sheets authentication
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
# client = gspread.authorize(creds)
# sheet_vote = client.open("Crowdsourcing-app").get_worksheet(0)
# sheet_feedback = client.open("Crowdsourcing-app").get_worksheet(1)

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
#         # st.write(feedback)

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
from oauth2client.service_account import ServiceAccountCredentials
from huggingface_hub import InferenceClient

# Load Hugging Face API token from environment variable
# HF_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
# if not HF_API_TOKEN:
#     st.error("Hugging Face API token is missing. Set HUGGINGFACE_API_TOKEN in your environment.")
#     st.stop()

# Load API token from secrets
HF_API_TOKEN = st.secrets["HUGGINGFACE_API_TOKEN"]

api = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.1")

# Load Google Cloud credentials from environment variable
google_credentials_json = os.getenv("GOOGLE_CREDENTIALS")
if not google_credentials_json:
    st.error("Google Cloud credentials are missing. Set GOOGLE_CREDENTIALS in your environment.")
    st.stop()

# Parse the JSON credentials from environment variable
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

        # Fetch and Display Votes
        st.subheader("Community Votes")
        vote = sheet_vote.col_values(1)
        feedback = sheet_feedback.col_values(1)

        # Summarize Feedback with Llama 3.1
        if len(vote) > 0:
            st.subheader("Feedback Summary")
            # Define input prompt
            prompt_vote = "You are a count checker. There are 2 photo options a user can place a vote for. Summarize the count of votes: " + str(vote)

            # Call the API
            response = api.chat_completion(messages=[{"role": "user", "content": prompt_vote}])
            
            # Extract the value from the 'content' key in the response
            if response and 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0]['message']['content']
                st.write(content)
            else:
                st.error("Failed to fetch a valid response from the API.")