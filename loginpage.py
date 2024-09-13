import streamlit as st
import yfinance as yf
from pymongo import MongoClient

# Set up MongoDB connection
client = MongoClient("mongodb+srv://himanshu:himanshu@user-database.tm5go.mongodb.net/?retryWrites=true&w=majority&appName=user-database")  # Change the URL if you're using a remote MongoDB server
db = client["user_database"]  # Database name
users_collection = db["users"]  # Collection for users
 
def display():
    # Fetch a user's watchlists
    def load_watchlists(username):
        """Load watchlists for the specified user from MongoDB."""
        user = users_collection.find_one({"username": username})
        if user and "watchlists" in user:
            return user["watchlists"]
        return {}

    def save_watchlist(username, name, tickers):
        """Save or update a watchlist for the user in MongoDB."""
        users_collection.update_one(
            {"username": username},
            {"$set": {f"watchlists.{name}": tickers}},
            upsert=True
        )

    def delete_watchlist(username, name):
        """Delete a watchlist for the user from MongoDB."""
        users_collection.update_one(
            {"username": username},
            {"$unset": {f"watchlists.{name}": ""}}
        )
    
    def delete_stock_from_watchlist(username, watchlist_name, ticker):
        """Remove a specific stock from a watchlist."""
        user = users_collection.find_one({"username": username})
        if user and "watchlists" in user and watchlist_name in user["watchlists"]:
            updated_tickers = [t for t in user["watchlists"][watchlist_name] if t != ticker]
            if updated_tickers:
                save_watchlist(username, watchlist_name, updated_tickers)
            else:
                delete_watchlist(username, watchlist_name)  # Remove the watchlist if empty

    def get_stock_data(ticker):
        """Fetch stock data for a given ticker."""
        try:
            stock = yf.Ticker(ticker)
            stock_info = stock.info
            # Fetching the most recent closing price
            history = stock.history(period='1d')
            latest_close = history['Close'].iloc[-1] if not history.empty else 'N/A'
            latest_close = f"{latest_close:.2f}" if isinstance(latest_close, float) else latest_close
            trailing_pe = stock_info.get('trailingPE', 'N/A')
            trailing_pe = f"{trailing_pe:.2f}" if isinstance(trailing_pe, float) else trailing_pe
            return {
                'Name': stock_info.get('shortName', 'N/A'),
                'Price': latest_close,
                'Market Cap': stock_info.get('marketCap', 'N/A'),
                'P/E Ratio': trailing_pe,
                '52 Week High': stock_info.get('fiftyTwoWeekHigh', 'N/A'),
                '52 Week Low': stock_info.get('fiftyTwoWeekLow', 'N/A'),
            }
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {e}")
            return None

    # Sign-in simulation
    if 'username' not in st.session_state:
        st.sidebar.header('Sign In')
        username = st.sidebar.text_input("Enter your username:", value="")
        if st.sidebar.button("Sign In"):
            if username:
                st.session_state['username'] = username
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Please enter a username.")
    else:
        username = st.session_state['username']
        st.markdown("<div class='header'>🔖 Stock Watchlist</div>",unsafe_allow_html=True)

        # Section to add, view, and delete watchlists
        st.sidebar.header('Manage Watchlists')
        
        watchlists = load_watchlists(username)
        
        def display_stock_data(stock_data):
            colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0", "#ffb3e6"]
            cols = st.columns(3)
            col_data = list(stock_data.items())
            for i, (key, value) in enumerate(col_data):
                color = colors[i % len(colors)]
                with cols[i % 3]:
                    st.markdown(f"<div style='color: {color}; font-weight: bold;'>{key}:</div> <div style='color: {color};'>{value}</div>", unsafe_allow_html=True)
        
        if watchlists:
            selected_watchlist = st.sidebar.selectbox("Select a watchlist to view:", options=list(watchlists.keys()) + ["Create New"])
            
            if selected_watchlist != "Create New":
                tickers = watchlists[selected_watchlist]
                with st.container():
                    st.subheader(f"{selected_watchlist}")
                    selected_ticker = st.selectbox("Select a stock to remove from this watchlist:", options=tickers)
                    
                    for ticker in tickers:
                        with st.expander(f"{ticker.upper()}"):
                            stock_data = get_stock_data(ticker)
                            if stock_data:
                                display_stock_data(stock_data)
                    if st.button(f"Remove "):
                        delete_stock_from_watchlist(username, selected_watchlist, selected_ticker)
                        st.success(f"Stock '{selected_ticker}' removed from watchlist '{selected_watchlist}' successfully!")
                        st.rerun()
                if st.sidebar.button(f"Delete {selected_watchlist}"):
                    delete_watchlist(username, selected_watchlist)
                    st.success(f"Watchlist '{selected_watchlist}' deleted successfully!")
                    st.rerun()
        else:
            st.write("No watchlists found.")
        
        # Section to create or update watchlists
        st.sidebar.header('Create or Update Watchlist')
        
        with st.sidebar.container():
            watchlist_name = st.text_input("Enter a name for your watchlist:")
            tickers_input = st.text_input("Enter stock tickers (comma-separated):")
        
            if st.button("Save Watchlist"):
                if watchlist_name and tickers_input:
                    tickers_list = [ticker.strip().upper() for ticker in tickers_input.split(',')]
                    save_watchlist(username, watchlist_name, tickers_list)
                    st.success(f"Watchlist '{watchlist_name}' saved successfully!")
                    st.rerun()
                else:
                    st.error("Please enter both a watchlist name and tickers.")
        
        st.sidebar.write("Enter a name and tickers to create or update a watchlist.")
        
        # Add custom CSS for animation
        st.markdown("""
            <style>
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            .stContainer > div {
                animation: fadeIn 1s ease-in-out;
            }
            </style>
            """, unsafe_allow_html=True)
