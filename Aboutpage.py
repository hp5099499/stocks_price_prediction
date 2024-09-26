def display():
    import streamlit as st
    with open("styles/style.css") as f:
      st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# def about_page():
    
    st.markdown("<div class='header'>What is StockAI?",unsafe_allow_html=True)
    st.markdown("""<p class='demp'>
        StockAI is an innovative platform designed to provide insights and analytics for stock market investments.
        Using advanced algorithms and machine learning models, StockAI helps users make markdownrmed decisions by analyzing 
        historical data, predicting market trends, and offering actionable insights.
        Our mission is to democratize stock market intelligence and make it accessible to both novice and experienced 
        investors. With StockAI, you can track stock performance, analyze market trends, and receive personalized 
        investment recommendations.
        <p>""",unsafe_allow_html=True)
    
    st.markdown("<div class='header'>Features",unsafe_allow_html=True)
    st.markdown("""<p style='margin:15px'>
        <br><b>Dashboard</b> - Visualize stock performance, market trends, and key metrics with interactive charts and graphs.
        <br><b>Stock Analysis</b> - Access detailed analyses of individual stocks, including historical performance and future predictions.
        <br><b>Personalized Recommendations</b> - Receive tailored investment suggestions based on your preferences and risk tolerance.
        <br><b>User-Friendly Interface</b> - Enjoy an intuitive and easy-to-use interface designed for both beginners and experienced investors.
        </p>""",unsafe_allow_html=True)
    
    st.markdown("<div class='header'>How It Works",unsafe_allow_html=True)
    st.markdown("""<p style='margin:15px'>
    Data Collection**: StockAI gathers and processes vast amounts of historical stock data and market markdownrmation.<br>
    Analysis**: Advanced algorithms analyze the data to identify patterns, trends, and investment opportunities.<br>
    Recommendations**: Based on the analysis, StockAI provides personalized recommendations to help users make better investment decisions.<br>
    Visualization**: Users can view and interact with various visualizations to understand market trends and stock performance.<br>
    </p>""",unsafe_allow_html=True)
    st.markdown("<div class='header'>Our Team",unsafe_allow_html=True)
    st.markdown("""<p style='margin:15px'>
        <span class='spl'>Himanshu Prajapati </span> - Financial analytics, database, data science and machine learning.<br>
        <span class='spl'>Mohit Maurya </span> - Software development, error handling and authentication.<br>
        <span class='spl'>Surajit Ghosh </span> - Focused on data analysis and front-end development.<br>
      
        """,unsafe_allow_html=True)
    
    st.markdown("<div class='header'>Contact Us",unsafe_allow_html=True)
    st.markdown("""<p style='margin:15px'>
        If you have any questions or feedback, feel free to reach out to us at:<br>
        Email: <a>support@stockai.com</a><br>
        Phone: +91 8090724228, 9310483653, 6294494643<br>
        Address: stockai, New Delhi, India, 110001<br>
        Follow us on :Twitter:<a>(https://twitter.com/stockai)</a><br> LinkedIn:<a>(https://linkedin.com/company/stockai)</a> for the latest updates!<br>
        </p>""",unsafe_allow_html=True)


