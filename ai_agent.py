import streamlit as st

def sales_chat(user_message: str) -> str:
    """
    Safe chat function that never crashes Streamlit Cloud.
    If no AI API key is configured, it returns a friendly message.
    """

    # Optional future AI integration
    # Example:
    # api_key = st.secrets.get("OPENAI_API_KEY")
    # if not api_key:
    #     return "AI chat is currently unavailable."

    if not user_message:
        return "Ask me anything about the product."

    return (
        "Thanks for your question! 👋\n\n"
        "This demo focuses on purchasing and instant delivery.\n"
        "AI chat will be enabled in a future update."
    )