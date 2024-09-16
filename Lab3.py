import streamlit as st
from openai import OpenAI

# Title of the app
st.title("Chatbot")

# Initialize OpenAI client with the secret API key
client = OpenAI(api_key=st.secrets["open_api_key"])

# Set the default model if not already present in session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize the messages list if not already in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask a question..."):
    # Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Check if the user is responding to "DO YOU WANT MORE INFO?"
    if len(st.session_state.messages) > 1 and st.session_state.messages[-2]["content"] == "DO YOU WANT MORE INFO?":
        # If user says "yes", provide more information
        if prompt.lower() == "yes":
            more_info = "Here is more detailed information on your question..."
            st.session_state.messages.append({"role": "assistant", "content": more_info})
            with st.chat_message("assistant"):
                st.markdown(more_info)

            # Re-ask the follow-up question
            follow_up = "DO YOU WANT MORE INFO?"
            st.session_state.messages.append({"role": "assistant", "content": follow_up})
            with st.chat_message("assistant"):
                st.markdown(follow_up)

        # If user says "no", ask for a new question
        elif prompt.lower() == "no":
            new_prompt = "What else can I help you with?"
            st.session_state.messages.append({"role": "assistant", "content": new_prompt})
            with st.chat_message("assistant"):
                st.markdown(new_prompt)

    else:
        # If the user is asking an initial question, generate assistant's response
        with st.chat_message("assistant"):
            # Create the completion
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            response = st.write_stream(stream)

        # Append assistant response to the session
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Ask "DO YOU WANT MORE INFO?" after the response
        follow_up = "DO YOU WANT MORE INFO?"
        st.session_state.messages.append({"role": "assistant", "content": follow_up})
        with st.chat_message("assistant"):
            st.markdown(follow_up)
