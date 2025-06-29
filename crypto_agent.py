


import os
import requests
import asyncio
import streamlit as st
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, function_tool

# Load environment variables
load_dotenv()
set_tracing_disabled(True)

# Get API key
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Define the tool function
@function_tool
def get_coin_info(symbol: str) -> str:
    """
    Get information about a cryptocurrency using its symbol (like BTC, ETH, etc).
    """
    url = "https://api.coinlore.net/api/tickers/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        coins = response.json().get("data", [])
        for coin in coins:
            if coin["symbol"].upper() == symbol.upper():
                return (
                    f"🪙 **{coin['name']} ({coin['symbol']})**\n"
                    f"💰 Price: ${coin['price_usd']}\n"
                    f"📊 Rank: {coin['rank']}\n"
                    f"📈 Change (24h): {coin['percent_change_24h']}%"
                )
        return f"❌ Coin with symbol '{symbol.upper()}' not found."
    except Exception as e:
        return f"❗ API Error: {e}"

# Create model provider
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

# Wrap model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

# Define agent
agent = Agent(
    name="CryptoCurrencyAgent",
    model=model,
    tools=[get_coin_info]
)

# Streamlit UI
st.set_page_config(page_title="Crypto Tool Agent", page_icon="🪙")
st.title("🪙 Gemini-Powered Crypto Tool Agent")

query = st.text_input("Ask about any crypto coin (e.g., What's the price of BTC?)")

if st.button("Ask") and query:
    with st.spinner("🤖 Thinking..."):
        try:
            # Fix: create and set a new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Call agent synchronously
            result = Runner.run_sync(
                agent,
                input=query,
            )
            st.markdown("### ✅ Response")
            st.success(result.final_output)
        except Exception as e:
            st.error(f"❌ Error: {e}")


