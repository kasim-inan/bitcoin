import streamlit as st
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

@st.cache(ttl=300)  # Cache for 5 minutes
def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['bitcoin']['usd']
    else:
        return None

@st.cache(ttl=300)  # Cache for 5 minutes
def get_historical_prices(days=30):
    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days={days}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        prices = data['prices']
        return [(datetime.fromtimestamp(int(item[0])/1000), item[1]) for item in prices]
    else:
        return None

def plot_price_chart(prices):
    if not prices:
        return None
    dates = [item[0] for item in prices]
    values = [item[1] for item in prices]
    
    plt.figure(figsize=(10, 4))
    plt.plot(dates, values, label="Bitcoin Price", color='orange')
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xlabel("Date")
    plt.ylabel("Price in USD")
    plt.title("Bitcoin Price Chart")
    plt.legend()
    plt.tight_layout()
    return plt

def main():
    st.title('Bitcoin Price Tracker')

    bitcoin_price = get_bitcoin_price()
    if bitcoin_price is not None:
        st.markdown(f"<h2 style='color: orange;'>The current price of Bitcoin is: ${bitcoin_price}</h2>", unsafe_allow_html=True)
    else:
        st.error("An error occurred while fetching the current Bitcoin price.")

    prices = get_historical_prices()
    if prices:
        fig = plot_price_chart(prices)
        if fig:
            st.pyplot(fig)
        else:
            st.error("Failed to plot the price chart.")
    else:
        st.error("An error occurred when fetching historical data.")

if __name__ == "__main__":
    main()
