# import streamlit as st
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from transformers import pipeline
# from PIL import Image
# import io

# # Load the Hugging Face summarization pipeline
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# # Google Sheets authentication
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
# client = gspread.authorize(creds)
# sheet = client.open("Crowdsourcing-app").sheet1

# # Streamlit App Interface
# st.title("Crowdsourced Feedback App")

# # Upload images for comparison
# st.subheader("Upload two images to compare")
# col1, col2 = st.columns(2)

# with col1:
#     image1 = st.file_uploader("Upload first image", type=["jpg", "png", "jpeg"], key="img1")
# with col2:
#     image2 = st.file_uploader("Upload second image", type=["jpg", "png", "jpeg"], key="img2")

# if image1 and image2:
#     col1, col2 = st.columns(2)
#     with col1:
#         img1 = Image.open(image1)
#         st.image(img1, caption="Image 1", use_container_width=True)
#     with col2:
#         img2 = Image.open(image2)
#         st.image(img2, caption="Image 2", use_container_width=True)
    
#     # Voting system
#     st.subheader("Vote for the better image")
#     vote = st.radio("Which image do you prefer?", ("Image 1", "Image 2"))
    
#     if st.button("Submit Vote"):
#         sheet.append_row([vote])
#         st.write("Your vote has been recorded!")

# # Display feedback from Google Sheets
# st.write("Feedback from the community:")
# feedback = sheet.col_values(1)
# st.write(feedback)

# # Summarize feedback using Llama 3.1
# if len(feedback) > 1:
#     st.write("Feedback Summary:")
#     combined_feedback = " ".join(feedback)
#     try:
#         summarized = summarizer(combined_feedback, max_length=150, min_length=50, do_sample=False)
#         st.write(summarized[0]['summary_text'])
#     except Exception as e:
#         st.write(f"Error while summarizing feedback: {e}")

# Version 2

# import streamlit as st
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from transformers import pipeline

# # Google Sheets authentication
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
# client = gspread.authorize(creds)
# sheet = client.open("Crowdsourcing-app").sheet1

# # Load summarization model
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# st.title("Crowdsourced Feedback App")

# # Upload images for comparison
# uploaded_images = []
# image1 = st.file_uploader("Upload first image", type=["jpg", "png", "jpeg"], key="image1")
# image2 = st.file_uploader("Upload second image", type=["jpg", "png", "jpeg"], key="image2")

# if image1 and image2:
#     uploaded_images.extend([image1, image2])
#     st.image([image1, image2], caption=["Image 1", "Image 2"], use_column_width=True)
#     st.session_state["images_uploaded"] = True
# else:
#     st.session_state["images_uploaded"] = False

# # Hide uploaders once images are uploaded
# if st.session_state.get("images_uploaded"):
#     st.write("Images uploaded successfully!")
# else:
#     image1 = None
#     image2 = None

# # User post dilemma
# post = st.text_area("Describe your dilemma here (e.g., which outfit looks better?)")
# if st.button("Post"):
#     if post:
#         sheet.append_row([post, "Pending", "Pending", "Pending"])
#         st.write("Your dilemma has been posted! Feedback will be gathered soon.")
#     else:
#         st.write("Please provide a dilemma description.")

# # Display feedback
# st.write("Feedback from the community:")
# feedback = sheet.col_values(1)
# st.write(feedback)

# # Summarize feedback
# if len(feedback) > 1:
#     st.write("Feedback Summary:")
#     summary = summarizer(" ".join(feedback), max_length=100, min_length=25, do_sample=False)[0]["summary_text"]
#     st.write(summary)


# Version 3
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
#         else:
#             st.warning("Please provide a dilemma description.")
    
#     # Hide upload box
#     st.markdown("<style>.stFileUploader {display: none;}</style>", unsafe_allow_html=True)

#     # Voting Buttons
#     if st.button("Vote for Option 1"):
#         sheet_vote.append_row(["Option 1", "1"])
#         st.success("You voted for Option 1!")

#     if st.button("Vote for Option 2"):
#         sheet_vote.append_row(["Option 2", "1"])
#         st.success("You voted for Option 2!")

# # Fetch and Display Votes
# st.subheader("Community Votes")
# vote = sheet_vote.col_values(1)
# feedback = sheet_feedback.col_values(1)
# # st.write(feedback)

# # Summarize Feedback with Llama 3.1
# if len(vote) > 0:
#     st.subheader("Feedback Summary")
#     # response = api(inputs="Summarize this feedback: " + str(feedback))
#     # Define input prompt
#     prompt_vote = "You are a count checker. There are 2 photo options a user can place a vote for. Summarize the count of votes: " + str(vote)

#     # Call the API
#     response = api.chat_completion(messages=[{"role": "user", "content": prompt_vote}])
#     st.write(response)



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

# # User Dilemma Post
# post = st.text_area("Describe your dilemma (e.g., which outfit looks better?)")
# dilemma_posted = st.session_state.get('dilemma_posted', False)

# if uploaded_images and len(uploaded_images) == 2:
#     if dilemma_posted:
#         # Display Dilemma Text above the images after posting
#         st.write(f"### Dilemma: {post}")
#         st.image(uploaded_images, caption=["Option 1", "Option 2"], width=300)

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
#     else:
#         # Show the dilemma input area before posting
#         if st.button("Post Dilemma"):
#             if post:
#                 sheet_feedback.append_row([post, "Pending"])
#                 st.success("Your dilemma has been posted!")
#                 st.session_state.dilemma_posted = True  # Set the state to True after posting
#             else:
#                 st.warning("Please provide a dilemma description.")

# # Hide upload box after dilemma is posted
# if dilemma_posted:
#     st.markdown("<style>.stFileUploader {display: none;}</style>", unsafe_allow_html=True)



import streamlit as st
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
from huggingface_hub import InferenceClient

# Load Hugging Face API token from environment variable
HF_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
if not HF_API_TOKEN:
    st.error("Hugging Face API token is missing. Set HUGGINGFACE_API_TOKEN in your environment.")
    st.stop()

api = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta")

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
