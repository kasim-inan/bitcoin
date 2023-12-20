'''
import streamlit as st
import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Function to fetch current Bitcoin price
def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data['bitcoin']['usd']

# Function to fetch historical Bitcoin prices
def get_historical_prices(days=30):
    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days={days}"
    response = requests.get(url)
    data = response.json()
    prices = data['prices']
    return [(datetime.fromtimestamp(int(item[0])/1000), item[1]) for item in prices]

# Function to plot the price chart
def plot_price_chart(prices):
    dates = [item[0] for item in prices]
    values = [item[1] for item in prices]
    plt.figure(figsize=(10, 4))
    plt.plot(dates, values, label="Bitcoin Price", color='orange')
    plt.xlabel("Date")
    plt.ylabel("Price in USD")
    plt.title("Bitcoin Price Chart")
    plt.legend()
    return plt

# Main function for the Streamlit app
def main():
    st.title('Bitcoin Price Tracker')

    # Display current Bitcoin price
    try:
        bitcoin_price = get_bitcoin_price()
        # Change the color and size of the current price display
        st.markdown(f"<h2 style='color: orange;'>The current price of Bitcoin is: ${bitcoin_price}</h2>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {e}")

    # Display historical Bitcoin price chart
    try:
        prices = get_historical_prices()
        fig = plot_price_chart(prices)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"An error occurred when fetching historical data: {e}")

# Ensuring the main function runs when the script is executed
if __name__ == "__main__":
    main()

    
'''


import streamlit as st
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Caching the response for a certain duration can prevent hitting API rate limits and improve performance
@st.cache(ttl=300)  # Cache for 5 minutes
def get_bitcoin_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()
        return data['bitcoin']['usd']
    except Exception as e:
        st.error(f"An error occurred while fetching current Bitcoin price: {e}")
        return None

@st.cache(ttl=300)  # Cache for 5 minutes
def get_historical_prices(days=30):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days={days}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        prices = data['prices']
        return [(datetime.fromtimestamp(int(item[0])/1000), item[1]) for item in prices]
    except Exception as e:
        st.error(f"An error occurred when fetching historical data: {e}")
        return []

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

    prices = get_historical_prices()
    if prices:
        fig = plot_price_chart(prices)
        if fig:
            st.pyplot(fig)
        else:
            st.error("Failed to plot the price chart.")

if __name__ == "__main__":
    main()
