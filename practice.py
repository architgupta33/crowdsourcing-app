# import openai

# client = openai.OpenAI(
#   api_key="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"
# )

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   # store=True,
#   messages=[
#     {"role": "user", "content": "write a haiku about ai"}
#   ]
# )

# print(completion.choices[0].message);






# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch

# # Load the Llama 2 model and tokenizer
# model_name = "meta-llama/Llama-3.1-8B"  # Or "meta-llama/Llama-2-13b-chat-hf"
# device = "cuda" if torch.cuda.is_available() else "cpu"

# # Load tokenizer and model
# print("Loading model...")
# tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=True)
# model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)

# # Chat function
# def chat_with_llama(prompt):
#     inputs = tokenizer(prompt, return_tensors="pt").to(device)
#     outputs = model.generate(
#         inputs["input_ids"],
#         max_length=256,
#         temperature=0.7,
#         top_p=0.9,
#         num_return_sequences=1
#     )
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return response

# # Example usage
# if __name__ == "__main__":
#     print("Llama 2 is ready!")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["quit", "exit"]:
#             print("Goodbye!")
#             break
#         response = chat_with_llama(user_input)
#         print(f"Llama 2: {response}")




# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# # Define the scope of the access
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# # Authenticate using the downloaded credentials
# creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

# # Authorize the client
# client = gspread.authorize(creds)

# # Open the Google Sheets document by its title
# sheet = client.open("Crowdsourcing-app").sheet1

# # Example: Get all values from the sheet
# data = sheet.get_all_records()
# print(data)


from huggingface_hub import InferenceClient
import os

# Get API key from environment
# api_key = os.getenv("HUGGINGFACE_API_TOKEN")

# Use the correct repo_id without specifying `task`
# api = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.1")

api = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta")


# Define input prompt
prompt = "What are the key benefits of using large language models?"

# Call the API
response = api.chat_completion(messages=[{"role": "user", "content": prompt}])
print(response)
