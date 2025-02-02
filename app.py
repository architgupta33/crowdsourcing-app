# import streamlit as st
# import gspread
# import os
# import json
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
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
            
#             # Plot Vote Results
#             # Vote Count
#             vote_counts = {"Option 1": vote.count("Option 1"), "Option 2": vote.count("Option 2")}

#             # Convert to DataFrame
#             df = pd.DataFrame(list(vote_counts.items()), columns=["Option", "Votes"])

#             st.subheader("Voting Visualization")
#             fig, ax = plt.subplots()
#             sns.barplot(x="Option", y="Votes", data=df, ax=ax, palette=["#1f77b4", "#ff7f0e"])
#             ax.set_title("Voting Visualization")
#             ax.set_ylabel("Number of Votes")
#             st.pyplot(fig)


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
api = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=HF_API_TOKEN)  # Add authentication token)

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
    sheet_vote = client.open("Crowdsourcing-app").get_worksheet(0)  # Votes worksheet
    sheet_feedback = client.open("Crowdsourcing-app").get_worksheet(1)  # Feedback worksheet
    sheet_comments = client.open("Crowdsourcing-app").get_worksheet(2)  # Comments worksheet
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
        # Voting and Comment Section
        st.subheader("Vote and Add a Comment")
        vote_option = st.radio("Choose your vote:", ["Option 1", "Option 2"])
        comment = st.text_area("Add a comment (optional):")

        if st.button("Submit Vote"):
            if vote_option:
                # Append vote to the Votes worksheet
                sheet_vote.append_row([vote_option])
                
                # Append comment to the Comments worksheet (if provided)
                if comment:
                    sheet_comments.append_row([vote_option, comment])
                    st.success(f"You voted for {vote_option} and your comment has been recorded!")
                else:
                    st.success(f"You voted for {vote_option}!")
            else:
                st.warning("Please select a vote option.")

        # Fetch and Display Votes
        # st.subheader("Community Votes")
        votes = sheet_vote.col_values(1)  # Fetch all votes

        if votes:
            # Summarize Feedback with Hugging Face API
            st.subheader("Feedback Summary")
            prompt_vote = "You are a count checker. There are 2 photo options a user can place a vote for. Summarize the count of votes: " + str(votes)
            
            # Call the API
            response = api.chat_completion(messages=[{"role": "user", "content": prompt_vote}])
            
            # Extract the value from the 'content' key in the response
            if response and 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0]['message']['content']
                st.write(content)
            else:
                st.error("Failed to fetch a valid response from the API.")

            # Fetch and Summarize Comments
            # st.subheader("Comments Summary")
            comments = sheet_comments.col_values(2)  # Fetch all comments (column 2)
            if comments:
                # Combine all comments into a single string
                comments_text = " ".join(comments)
                
                # Generate a summary using Hugging Face API
                prompt_summary = f"Summarize the following user comments in 2-3 sentences: {comments_text}"
                summary_response = api.chat_completion(messages=[{"role": "user", "content": prompt_summary}])
                
                # Display the summary
                if summary_response and 'choices' in summary_response and len(summary_response['choices']) > 0:
                    summary = summary_response['choices'][0]['message']['content']
                    st.write(summary)
                else:
                    st.error("Failed to generate a summary of comments.")
            else:
                st.info("No comments yet.")
            
            # Plot Vote Results
            vote_counts = {"Option 1": votes.count("Option 1"), "Option 2": votes.count("Option 2")}

            # Convert to DataFrame
            df = pd.DataFrame(list(vote_counts.items()), columns=["Option", "Votes"])

            st.subheader("Voting Visualization")
            fig, ax = plt.subplots()
            sns.barplot(x="Option", y="Votes", data=df, ax=ax, palette=["#1f77b4", "#ff7f0e"])
            ax.set_title("Voting Visualization")
            ax.set_ylabel("Number of Votes")
            st.pyplot(fig)

            