import streamlit as st
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

# Azure configuration
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"
token = os.environ.get("GITHUB_TOKEN")  # Use .get() to avoid KeyError if not set

if not token:
    st.error("Azure API token is not set. Please configure the GITHUB_TOKEN environment variable.")
    st.stop()

# Initialize Azure ChatCompletionsClient
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

# Streamlit app title
st.title("Joke Explainer")

# Text input for the joke
joke = st.text_input("Enter your joke here:")

# Submit button
if st.button("Submit"):
    if joke:
        # Call the Azure API to get the explanation
        try:
            response = client.complete(  # Correct method name
                model=model_name,
                messages=[
                    {"role": "user", "content": f"Explain this joke: {joke}"}
                ]
            )
            explanation = response.choices[0].message.content
            # Display the explanation
            st.subheader("Explanation")
            st.write(explanation)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a joke before submitting.")