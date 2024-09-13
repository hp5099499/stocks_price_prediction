import streamlit as st
import pandas as pd
def display():
    df=pd.read_csv("equity_issuers.csv")
    
    # Get the list of unique sectors
    unique_sectors = df['Sector Name'].drop_duplicates().tolist()
    
    # Streamlit selectbox for sector selection
    selected_sector = st.sidebar.selectbox("Select a Sector", unique_sectors)
    
    # Filter DataFrame based on selected sector
    filtered_df = df[df['Sector Name'] == selected_sector]
    
    # Display the filtered stock names
    st.table(filtered_df[['Security Code']])
    
    from yahooquery import Ticker
    # stock_name=st.text_input("enter the stock name:")
    def get_ticker_from_name(stock_name):
        search = Ticker(stock_name)
        symbols = search.symbols
    
        if symbols:
            # Return the first matching ticker
            st.write(symbols[0])
        else:
             st.write("Ticker not found")
    