import streamlit as st
from openai import OpenAI

# Setup OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"]
)

# Streamlit UI
st.title("📈 Crypto Agent (OpenRouter-Powered)")

user_query = st.text_input("Ask about a crypto coin (e.g., What's the price of BTC?)")

if st.button("Ask") and user_query:
    try:
        # Step 1: Let LLM extract the symbol from user input
        extract_prompt = f"""
From the user's message below, extract only the crypto symbol (like BTC, ETH, DOGE):
"{user_query}"
Just respond with the symbol, nothing else.
"""

        symbol_response = client.chat.completions.create(
            model="mistralai/mistral-nemo:free",
            messages=[
                {"role": "user", "content": extract_prompt}
            ]
        )

        symbol = symbol_response.choices[0].message.content.strip().upper()

        # Step 2: Use our tool function
        from coin_tool import get_coin_info  # or define get_coin_info above
        result = get_coin_info(symbol)

        # Step 3: Show the result
        st.markdown("### ✅ Result:")
        st.markdown(result)

    except Exception as e:
        st.error(f"Error: {e}")
