import streamlit as st
from openai import OpenAI
import os

# Show title and description
st.title("📄 Document Summarizer")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys)."
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.secrets["open_api_key"]
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader("Upload a document (.txt or .md)", type=("txt", "md"))

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    # Sidebar options for different types of summaries
    st.sidebar.title("Summary Options")
    summary_option = st.sidebar.radio(
        "Select the type of summary you'd like:",
        (
            "Summarize in 100 words",
            "Summarize in 2 paragraphs",
            "Summarize in 5 bullet points"
        )
    )

    # Checkbox for using advanced GPT-4 model
    use_advanced_model = st.sidebar.checkbox("Use Advanced Model (GPT-4)")

    # Choose model based on checkbox
    selected_model = "gpt-4" if use_advanced_model else "gpt-3.5-turbo"

    if uploaded_file and question:

        # Process the uploaded file and question.
        document = uploaded_file.read().decode()

        # Adjust the prompt based on the selected summary option
        if summary_option == "Summarize in 100 words":
            summary_instruction = "Summarize the document in about 100 words."
        elif summary_option == "Summarize in 2 paragraphs":
            summary_instruction = "Summarize the document in 2 connecting paragraphs."
        else:
            summary_instruction = "Summarize the document in 5 bullet points."

        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {summary_instruction}",
            }
        ]

        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model=selected_model,
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)
