import streamlit as st
from pymongo import MongoClient
import hashlib, uuid
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from streamlit_navigation_bar import st_navbar
with open("styles/style.css") as f:
      st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def scrape_top_losers():
    url = "https://groww.in/markets/top-losers"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find('table')
    if not table:
        return []
    
    headers = [header.get_text() for header in table.find_all('th')]
    rows = [
        dict(zip(headers, [col.get_text(strip=True) for col in row.find_all('td')]))
        for row in table.find_all('tr')[1:] if row.find_all('td')
    ]
    return rows

# Function to get tickers from company names using Yahoo Query
def get_tickers_from_names(companies):
    tickers = {}
    for company in companies:
        try:
            results = search(company).get('quotes', [])
            tickers[company] = results[0]['symbol'] if results else None
        except Exception:
            tickers[company] = None
    return tickers

# Function to fetch stock data using YFinance
def fetch_stock_data(tickers):
    data = {}
    for company, symbol in tickers.items():
        if not symbol:
            data[company] = {key: None for key in ['Open Price', 'High Price', 'Low Price', 'Previous Close', 'Close', 'Change (%)']}
            continue
        
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period='5d')
            if len(hist) >= 2:
                prev_close = hist['Close'].iloc[-2]
                curr_close = hist['Close'].iloc[-1]
                change = curr_close - prev_close
                data[company] = {
                    'Open Price': f"{hist['Open'].iloc[-1]:.2f}",
                    'High Price': f"{hist['High'].iloc[-1]:.2f}",
                    'Low Price': f"{hist['Low'].iloc[-1]:.2f}",
                    'Previous Close': f"{prev_close:.2f}",
                    'Close': f"{curr_close:.2f}",
                    'Change (%)': f"{(change / prev_close) * 100:.2f}"
                }
            else:
                data[company] = {key: None for key in ['Open Price', 'High Price', 'Low Price', 'Previous Close', 'Close', 'Change (%)']}
        except Exception as e:
            st.error(f"Error fetching data for {company}: {e}")
            data[company] = {key: None for key in ['Open Price', 'High Price', 'Low Price', 'Previous Close', 'Close', 'Change (%)']}
    
    return data

# Function to fetch real-time index data
# Streamlit layout for displaying Top Losers
@st.cache_data(ttl=86400)  # Cache data for 86400 seconds (1 day)
def get_loser_data():
    data = scrape_top_losers()
    if data:
        companies = [item['Company'] for item in data]
        tickers = get_tickers_from_names(companies)
        stock_data = fetch_stock_data(tickers)
        table = [{
            "Symbol": symbol,
            "Open Price": stock_info['Open Price'],
            "High Price": stock_info['High Price'],
            "Low Price": stock_info['Low Price'],
            "Previous Close": stock_info['Previous Close'],
            "Close": stock_info['Close'],
            "Change (%)": stock_info['Change (%)']
        } for symbol, stock_info in stock_data.items()]
        return table
    else:
        return []

# Function to display the cached data
def display_losers():
    with st.spinner('Loading data...'):
        table = get_loser_data()
        if table:
            df = pd.DataFrame(table)
            df.index += 1  # Add index starting from 1
            st.table(df)
        else:
            st.write('No data found or unable to fetch data.')

def analysis():
    import streamlit as st
    import pandas as pd
    import yfinance as yf
    from datetime import datetime, timedelta
    import plotly.graph_objects as go
    from ta.volatility import BollingerBands
    from ta.trend import MACD, EMAIndicator, SMAIndicator
    from ta.momentum import RSIIndicator
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score, mean_absolute_error
    import time
    
    
    # st.subheader('Stock Price Predictions')
    
    def main():
        option = st.sidebar.selectbox('Make a choice', ['Visualize', 'Recent Data', 'Predict'])
        if option == 'Visualize':
            tech_indicators()
        elif option == 'Recent Data':
            update_data_and_plot()
            # st.markdown("[more...](https://predictre.streamlit.app)")
    
        elif option == 'Predict':
            predict()
        
    
    @st.cache_resource
    def download_data(op, start_date, end_date):
        df = yf.download(op, start=start_date, end=end_date, progress=False)
        return df
    
    option = st.sidebar.text_input('Enter a Stock Symbol', value='SPY')
    option = option.upper()
    today = datetime.today().date()
    duration = st.sidebar.number_input('Enter the duration', value=3000)
    before = today - timedelta(days=duration)
    start_date = st.sidebar.date_input('Start Date', value=before)
    end_date = st.sidebar.date_input('End date', today)
    if st.sidebar.button('Send'):
        if start_date < end_date:
            st.sidebar.success('Start date: `%s`\n\nEnd date: `%s`' % (start_date, end_date))
            data = download_data(option, start_date, end_date)
        else:
            st.sidebar.error('Error: End date must fall after start date')
    
    data = download_data(option, start_date, end_date)
    scaler = StandardScaler()
    
    # Compute the price difference and percentage change
    p_d = data.Close.iloc[-1] - data.Open.iloc[1]
    pd_p = (p_d / data.Open.iloc[1]) * 100
    
    def tech_indicators():
        st.markdown("<div class='header'>Technical Indicators</div>", unsafe_allow_html=True)
        option = st.radio('Choose a Technical Indicator to Visualize', ['Close', 'BB', 'MACD', 'RSI', 'SMA', 'EMA'])
    
        # Bollinger bands
        bb_indicator = BollingerBands(data.Close)
        bb = data.copy()
        bb['bb_h'] = bb_indicator.bollinger_hband()
        bb['bb_l'] = bb_indicator.bollinger_lband()
        # Creating a new dataframe
        bb = bb[['Close', 'bb_h', 'bb_l']]
        # MACD
        macd = MACD(data.Close).macd()
        # RSI
        rsi = RSIIndicator(data.Close).rsi()
        # SMA
        sma = SMAIndicator(data.Close, window=14).sma_indicator()
        # EMA
        ema = EMAIndicator(data.Close).ema_indicator()
    
        if option == 'Close':
            st.write('Close Price')
            st.line_chart(data['Close'])
        elif option == 'BB':
            st.write('BollingerBands')
            st.line_chart(bb)
        elif option == 'MACD':
            st.write('Moving Average Convergence Divergence')
            st.line_chart(macd)
        elif option == 'RSI':
            st.write('Relative Strength Indicator')
            st.line_chart(rsi)
        elif option == 'SMA':
            st.write('Simple Moving Average')
            st.line_chart(sma)
        else:
            st.write('Exponential Moving Average')
            st.line_chart(ema)
    
    def fetch_stock_data(ticker, period="1d", interval="1m"):
        return yf.Ticker(ticker).history(period=period, interval=interval)
    
    def update_data_and_plot():
        st.markdown("<div class='header'>Real Time Data</div>",unsafe_allow_html=True)
        
        ticker=option
        time_range = st.selectbox("Select the time range:", ["1d"])
    
        # Time range mapping
        time_range_map = {
            "1d": ("1d", "5m"),
        }
    
        if ticker and time_range:
            period, interval = time_range_map.get(time_range, ("1d", "5m"))
            data = fetch_stock_data(ticker, period, interval)
    
            # Initialize session state
            if "historical_data" not in st.session_state:
                st.session_state.historical_data = pd.DataFrame()
            if "last_data_point" not in st.session_state:
                st.session_state.last_data_point = None
            if "same_data_time" not in st.session_state:
                st.session_state.same_data_time = None
            if "last_update_time" not in st.session_state:
                st.session_state.last_update_time = datetime.now()
            if "auto_update" not in st.session_state:
                st.session_state.auto_update = False
            if "update_stopped" not in st.session_state:
                st.session_state.update_stopped = False
    
            chart_placeholder = st.empty()
            table_placeholder = st.empty()
    
            def update_data_and_plot():
                new_data = fetch_stock_data(ticker, period, interval)
                if not new_data.empty:
                    current_data_point = new_data.iloc[-1]['Close']
                    if st.session_state.last_data_point == current_data_point:
                        if st.session_state.same_data_time is None:
                            st.session_state.same_data_time = datetime.now()
                        elif datetime.now() - st.session_state.same_data_time > timedelta(minutes=5):
                            st.write("Data unchanged for 5 minutes. Stopping updates.")
                            st.session_state.auto_update = False
                            st.session_state.update_stopped = True
                            return
                    else:
                        st.session_state.same_data_time = None
    
                    st.session_state.last_data_point = current_data_point
                    st.session_state.historical_data = pd.concat([st.session_state.historical_data, new_data]).drop_duplicates()
    
                    fig = go.Figure(data=[go.Candlestick(
                        x=st.session_state.historical_data.index,
                        open=st.session_state.historical_data['Open'],
                        high=st.session_state.historical_data['High'],
                        low=st.session_state.historical_data['Low'],
                        close=st.session_state.historical_data['Close'],
                        increasing_line_color='green',
                        decreasing_line_color='red'
                    )])
                    fig.update_layout(title=f"{ticker} - Real-Time Data", xaxis_title="Time", yaxis_title="Price")
                    chart_placeholder.plotly_chart(fig, use_container_width=True)
                    st.session_state.last_update_time = datetime.now()
                    st.session_state.update_stopped = False
                    table_placeholder.dataframe(st.session_state.historical_data)
    
            if st.button("Live data"):
                st.session_state.auto_update = True
                st.session_state.update_stopped = False
    
            if st.button("Stop"):
                st.session_state.auto_update = False
                st.session_state.update_stopped = True
    
            if st.session_state.auto_update:
                 update_data_and_plot()
                 time.sleep(15)
                 if st.session_state.auto_update:  # Ensure re-run only when auto-update is True
                    st.rerun()
    
    
            if st.session_state.update_stopped:
                st.write("Updates have stopped. Showing the last updated data.")
                fig = go.Figure(data=[go.Candlestick(
                    x=st.session_state.historical_data.index,
                    open=st.session_state.historical_data['Open'],
                    high=st.session_state.historical_data['High'],
                    low=st.session_state.historical_data['Low'],
                    close=st.session_state.historical_data['Close'],
                    increasing_line_color='green',
                    decreasing_line_color='red'
                )])
              
                fig.update_layout(title=f"{ticker} - Last Updated Data", xaxis_title="Time", yaxis_title="Price")
                chart_placeholder.plotly_chart(fig, use_container_width=True)
                table_placeholder.dataframe(st.session_state.historical_data)
                high=st.session_state.historical_data['High'],
                low=st.session_state.historical_data['Low'],
                # Assuming 'historical_data' is a DataFrame stored in session state
                close = st.session_state.historical_data['Close']
                
                # Get the latest value
                latest_value = close.iloc[-1]
                
                # Create a slider that ranges from the minimum to maximum value of 'Close'
                # You can set the default value to the latest value

    
    def predict():
        st.markdown("<div class='header'>Stock Price Prediction</div>",unsafe_allow_html=True)

        num = st.number_input('How many days forecast?', value=5)
        num = int(num)
        if st.button('Predict'):
            model_engine(num)
    
    def model_engine(num):
        # getting only the closing price
        df = data[['Close']]
        # shifting the closing price based on number of days forecast
        df['preds'] = data.Close.shift(-num)
        # scaling the data
        x = df.drop(['preds'], axis=1).values
        x = scaler.fit_transform(x)
        # storing the last num_days data
        x_forecast = x[-num:]
        # selecting the required values for training
        x = x[:-num]
        # getting the preds column
        y = df.preds.values
        # selecting the required values for training
        y = y[:-num]
    
        # splitting the data
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.2, random_state=7)
        # training the model
        model = LinearRegression()
        model.fit(x_train, y_train)
        preds = model.predict(x_test)
        col1, col2 = st.columns(2)
        with col1:
            st.info(f'Accuracy score: {r2_score(y_test, preds) * 100:.2f}%')
        with col2:
            st.info(f'MAE: {mean_absolute_error(y_test, preds):.2f}')
        # predicting stock price based on the number of days
        forecast_pred = model.predict(x_forecast)
        forecast_dates = pd.date_range(start=data.index[-1], periods=num + 1).tolist()[1:]
        forecast_df = pd.DataFrame(forecast_pred, index=forecast_dates, columns=['Forecast'])
    
        # Combine historical data with forecast data
        combined_df = pd.concat([data[['Close']], forecast_df])
    
        st.line_chart(combined_df)
    
    if __name__ == '__main__':
        main()


# CSS for styling sidebar
centered_content_css = """
    <style>
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        hr {
            border: 1px solid #333;
        }
    </style>
"""

# Navbar function
# def st_navbar(options):
#     selected = st.sidebar.radio("Navigation", options)
#     return selected

# # MongoDB connection setup
# client = MongoClient("mongodb://localhost:27017")
# db = client["user_database"]
# users_collection = db["users"]
# reset_tokens_collection = db["reset_tokens"]


# Create the MongoDB URI using the credentials
client = MongoClient("mongodb+srv://himanshu:himanshu@user-database.tm5go.mongodb.net/?retryWrites=true&w=majority&appName=user-database")
db = client["user_database"]
users_collection = db["users"]
reset_tokens_collection = db["reset_tokens"]# Placeholder logout function
def logout():
    st.session_state['logged_in'] = False
    st.rerun()

# Validate email with regex
def validate_email(email):
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_pattern, email)

# Validate password with regex (at least 8 characters, digit, uppercase, special character)
def validate_password(password):
    password_pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(password_pattern, password)

# Hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Send email with a reset token link
def send_reset_email(user_email, token):
    sender_email = "himanshupra67@gmail.com"
    sender_password = "qcfa vuzq oqpd tdzf"
    receiver_email = user_email

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'Password Reset Request'

    reset_link = f"http://localhost:8501/?token={token}&email={user_email}"
    body = f"Hi,\n\nClick the link below to reset your password:\n{reset_link}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Start TLS for security
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

# Save user data to MongoDB
def save_user_data(email, username, hashed_password):
    user = users_collection.find_one({"email": email})
    if user:
        users_collection.update_one({"email": email}, {"$set": {"password": hashed_password}})
    else:
        users_collection.insert_one({"email": email, "username": username, "password": hashed_password})

# Save reset token to MongoDB
def save_reset_token(token, email):
    reset_tokens_collection.insert_one({"token": token, "email": email})

# Delete reset token from MongoDB
def delete_reset_token(token):
    reset_tokens_collection.delete_one({"token": token})

# Sign-up function
def signup():
    st.markdown("<div class='header'>Sign up</div>",unsafe_allow_html=True)

    username = st.text_input("Username", key="signup_username")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
    
    if st.button("Sign Up", key="signup_button"):
        if not validate_email(email):
            st.error("Invalid email address.")
        elif not validate_password(password):
            st.error("Password must be at least 8 characters long, include one digit, one uppercase letter, and one special character.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            user = users_collection.find_one({"email": email})
            if user:
                st.error("Email already registered.")
            else:
                hashed_password = hash_password(password)
                save_user_data(email, username, hashed_password)
                st.success("Sign up successful! You can now log in.")
                st.session_state['redirect_to_signin'] = True
                st._rerun()

# Sign-in function
def signin():
    st.markdown("<div class='header'>Sign in</div>",unsafe_allow_html=True)

    email = st.text_input("Email", key="signin_email")
    password = st.text_input("Password", type="password", key="signin_password")
    
    if st.button("Sign In", key="signin_button"):
        user = users_collection.find_one({"email": email})
        if user:
            hashed_password = hash_password(password)
            if user["password"] == hashed_password:
                st.success(f"Welcome back, {user['username']}!")
                st.session_state["logged_in"] = True
                st.session_state["username"] = user["username"]
                st.rerun()
            else:
                st.error("Invalid email or password.")
        else:
            st.error("Email not registered.")

# Password reset request function
# def reset_password():
   
# Password reset using token
def reset_password():
    st.markdown("<div class='header'>Forget Password</div>",unsafe_allow_html=True)

    reset_email = st.text_input("Enter your email to reset your password", key="reset_email")
    
    if st.button("Send Reset Link", key="send_reset_link"):
        user = users_collection.find_one({"email": reset_email})
        if user:
            token = str(uuid.uuid4())
            save_reset_token(token, reset_email)
            send_reset_email(reset_email, token)
            st.success("A password reset link has been sent to your email.")
        else:
            st.error("Email not registered.")

    token = st.query_params.get('token', [None])
    email = st.query_params.get('email', [None])
    
    reset_token = reset_tokens_collection.find_one({"token": token, "email": email})

    if reset_token:
        new_password = st.text_input("New Password", type="password", key="new_password")
        confirm_new_password = st.text_input("Confirm New Password", type="password", key="confirm_new_password")
        
        if new_password and confirm_new_password:
            if new_password == confirm_new_password:
                hashed_password = hash_password(new_password)
                save_user_data(email, None, hashed_password)
                delete_reset_token(token)
                st.success("Password has been reset. You can now log in.")
                
            else:
                st.error("Passwords do not match.")
    # else:
    #     st.error("Invalid or expired reset link.")

# Main logic for showing the right form based on state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if 'redirect_to_signin' in st.session_state and st.session_state['redirect_to_signin']:
    st.session_state['redirect_to_signin'] = False
    st.rerun()

# Inject CSS and create sidebar
# st.sidebar.markdown(centered_content_css, unsafe_allow_html=True)

if st.session_state["logged_in"]:
    import logo
    logo.display()
    centered_content_css = f"""
    <style>
        .centered-content {{
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }}
                .welcome-text {{
            margin-bottom: 20px;
            text-align: center;
        }}
    </style>
    <div class="welcome-text">
        <h3 style='color:green;'>Welcome, {st.session_state["username"].upper()}!</h3>
        <p style='text-align:center'>You have successfully logged into StockAi</p>
    </div>
    <div>
           </div>
"""

# Inject the CSS and HTML into the sidebar
    st.sidebar.markdown(centered_content_css, unsafe_allow_html=True)

    st.sidebar.button("Logout", on_click=logout)
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    
    # Navbar with multiple pages
    choice = st_navbar(["Home", "Dashboard", "Analysis", "About", "Watchlist", "Setting"])

    if choice == "Home":
        
        import pthon
        pthon.main()
        # st.markdown("<div class='header'>Top Gainers</div>",unsafe_allow_html=True)
        # pthon.fetch_gainers()
        # st.markdown("<div class='header'>Top Losers</div>",unsafe_allow_html=True)
        # pthon.display_losers()
        # st.markdown("<div class='header'>Indices</div>",unsafe_allow_html=True)
        # pthon.display_indices()

    elif choice == "Dashboard":
        st.markdown("<div class='header'>Stock Dashboard</div>",unsafe_allow_html=True)
        import Homepage
        Homepage.display()

    elif choice == "Analysis":
        analysis()

    elif choice == "About":

        import Aboutpage
        Aboutpage.display()

    elif choice == "Watchlist":
        col1, col2 = st.tabs(["Watchlist", "Know your Stock"])
        with col1:
            import loginpage
            loginpage.display()

        with col2:
            import info
            st.markdown("<div class='header'>Sector-wise Stocks</div>",unsafe_allow_html=True)

            info.display()

    elif choice == "Setting":
        import setting
        setting.main()

else:
    # Navbar for unauthenticated users
    choice = st_navbar(["Home", "Account"])

    if choice == "Home":
        import home1
        home1.main()

    elif choice == "Account":
        option = st.sidebar.selectbox('Options', ['Signin', 'Signup', 'Reset Password'])

        if option == 'Signup':
            signup()

        elif option == 'Signin':
            signin()
            

        elif option == 'Reset Password':
            reset_password()
