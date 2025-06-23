import requests

def get_coin_info(symbol: str) -> str:
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