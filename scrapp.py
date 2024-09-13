import streamlit as st
import yfinance as yf
from yahooquery import search
import pandas as pd
import json

# Function to get tickers based on company names
def get_tickers_from_names(companies):
    tickers = {}
    for company in companies:
        try:
            search_results = search(company)
            # Display search results for debugging in the Streamlit app
            st.write(f"Search results for {company}: {search_results}")
            
            # Verify if the search results are in the expected format
            if isinstance(search_results, dict) and 'quotes' in search_results:
                if search_results['quotes']:
                    ticker = search_results['quotes'][0]['symbol']
                    tickers[company] = ticker
                else:
                    tickers[company] = None
            else:
                tickers[company] = None

        except json.JSONDecodeError as e:
            st.write(f"JSON decoding error for {company}: {e}")
            tickers[company] = None
        except Exception as e:
            st.write(f"Error during search for {company}: {e}")
            tickers[company] = None
    return tickers

# Function to fetch stock data
def fetch_stock_data(tickers):
    all_data = {}
    for company, symbol in tickers.items():
        if symbol:
            try:
                stock = yf.Ticker(symbol)
                data = stock.history(period='5d')
                
                if len(data) >= 2:
                    # Extracting necessary data
                    previous_close = data['Close'].iloc[-2]
                    current_close = data['Close'].iloc[-1]
                    change = current_close - previous_close
                    percent_change = (change / previous_close) * 100
                    
                    # Adding more details
                    open_price = data['Open'].iloc[-1]
                    high_price = data['High'].iloc[-1]
                    low_price = data['Low'].iloc[-1]
                    
                    all_data[company] = {
                        'Open Price': open_price,
                        'High Price': high_price,
                        'Low Price': low_price,
                        'Previous Close': previous_close,
                        'Close': current_close,
                        'Change (%)': percent_change
                    }
                else:
                    all_data[company] = {
                        'Open Price': None,
                        'High Price': None,
                        'Low Price': None,
                        'Previous Close': None,
                        'Close': None,
                        'Change (%)': None
                    }
            except Exception as e:
                st.error(f"Error fetching data for {company}: {e}")
                all_data[company] = {
                    'Open Price': None,
                    'High Price': None,
                    'Low Price': None,
                    'Previous Close': None,
                    'Close': None,
                    'Change (%)': None
                }
        else:
            all_data[company] = {
                'Open Price': None,
                'High Price': None,
                'Low Price': None,
                'Previous Close': None,
                'Close': None,
                'Change (%)': None
            }
    return all_data

# Streamlit app
if __name__ == "__main__":
    st.title("Stock Data Viewer")

    companies = ["Avenue Supermarts", "Berger Paints India", "Cholamandalam Investment & Finance Company"]
    tickers = get_tickers_from_names(companies)
    stock_data = fetch_stock_data(tickers)

    # Convert the data to a DataFrame and reset the index to include it as a column
    df = pd.DataFrame(stock_data).T.reset_index()
    df.columns = ['Company', 'Open Price', 'High Price', 'Low Price', 'Previous Close', 'Close', 'Change (%)']

    # Display the data in a tabular format
    st.write("### Stock Data")
    st.dataframe(df, width=800)  # Adjust the width as needed
