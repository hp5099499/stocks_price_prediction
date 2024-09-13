import json
import os
from PIL import Image
import base64
import streamlit as st

# Function to display marquee
def display_marquee():
    st.markdown("""
    <style>
        /* Marquee Container */
        .marquee-container {
            position: relative;
            width: 100%;
            overflow: hidden;
            background-color: #4CAF50;
            color: white;
            padding: 10px 0;
            border-radius: 8px;
        }
        /* Marquee Text */
        .marquee-content {
            display: inline-block;
            white-space: nowrap;
            padding-left: 100%;
            font-size: 18px;
            font-family: 'Poppins', sans-serif;
            animation: marquee 15s linear infinite;
        }
        /* Smooth marquee animation */
        @keyframes marquee {
            0% {
                transform: translateX(100%);
            }
            100% {
                transform: translateX(-100%);
            }
        }
        /* Pause on hover */
        .marquee-container:hover .marquee-content {
            animation-play-state: paused;
        }
        /* Responsive adjustments */
        @media screen and (max-width: 768px) {
            .marquee-content {
                font-size: 14px;
            }
        }
    </style>
    <div class="marquee-container">
        <div class="marquee-content">
            Welcome to StockAI! Let's come together and dream big. Unleashing the power of AI to reshape the future of stock trading.
        </div>
    </div>
    """, unsafe_allow_html=True)


def get_base64_image(img_path):
    try:
        with open(img_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        return None

# Load and encode logo image
logo_path = 'logo.jpg'  # Path to your logo image
logo_base64 = get_base64_image(logo_path)


if logo_base64:
    def display_header():
        st.markdown(f"""
        <style>
            /* Global CSS for the header */
            .header {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                background: rgba(76, 175, 80, 0.9); /* Added transparency */
                border-radius: 8px;
                padding: 20px 40px;
                color: white;
                text-align: center;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* Adds depth */
            }}
            .header img {{
                height: 70px;
                margin-right: 20px;
            }}
            .header-content {{
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                text-align: left;
            }}
            .header h1 {{
                font-size: 50px;
                font-family: 'Poppins', sans-serif; /* Custom font */
                margin: 0;
                font-weight: bold;
            }}
            .header h2 {{
                font-size: 20px;
                margin-top: 8px;
                color: #E0F2F1;
                font-style: italic;
            }}
            .header-buttons {{
                display: flex;
                gap: 15px;
            }}
            .header-button {{
                background-color: white;
                color: #4CAF50;
                padding: 10px 20px;
                border-radius: 25px;
                text-decoration: none;
                font-weight: bold;
                transition: background-color 0.3s ease, color 0.3s ease;
            }}
            .header-button:hover {{
                background-color: #229954;
                color: white;
            }}
            .social-icons {{
                display: flex;
                gap: 10px;
                margin-top: 10px;
            }}
            .social-icons a {{
                color: white;
                font-size: 30px;
                transition: color 0.3s ease;
            }}
            .social-icons a:hover {{
                color: #FFC107;
            }}
            /* Responsive Design */
            @media screen and (max-width: 768px) {{
                .header h1 {{
                    font-size: 36px;
                }}
                .header h2 {{
                    font-size: 16px;
                }}
                .header img {{
                    height: 50px;
                }}
                .header {{
                    padding: 15px 20px;
                }}
                .header-buttons {{
                    flex-direction: column;
                    gap: 10px;
                }}
            }}
        </style>
        <div class="header">
            <!-- Logo and Main Title -->
            <div class="header-content">
                <h1><img src="data:image/jpeg;base64,{logo_base64}" alt="Logo"/>StockAI</h1>
                <h2>Empowering your financial future with AI-driven insights</h2>
                <div class="social-icons">
                    <a href="#"><i class="fab fa-facebook"></i></a>
                    <a href="#"><i class="fab fa-twitter"></i></a>
                    <a href="#"><i class="fab fa-linkedin"></i></a>
                </div>
            </div>
            <!-- Action Buttons -->
            <div class="header-buttons">
                <a class="header-button" href="#">Home</a>
                <a class="header-button" href="#">Account</a>
            </div>
        </div>
        """, unsafe_allow_html=True)


#Font Awesome or Google Fonts in the app's header
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    """, unsafe_allow_html=True)


# Function to display About section
def display_about():
    st.write("""
             <div style="text-align: center; margin-top: 40px;">
             <h2>About StockAI</h2>
             <p>
             <b>StockAI</b> is an innovative platform designed to provide insights and analytics for stock market investments.
             Using advanced algorithms and machine learning models, StockAI helps users make informed decisions by analyzing 
             historical data, predicting market trends, and offering actionable insights.
             Our mission is to democratize stock market intelligence and make it accessible to both novice and experienced 
             investors. With StockAI, you can track stock performance, analyze market trends, and receive personalized 
             investment recommendations.
             </p>
             </div>
             
    """,unsafe_allow_html=True)


    if st.button('Read More'):
        st.markdown("""
        <style>
        .flex-container {
            display: flex;
            gap: 20px;
        }
        .box {
            background-color: transparent;
            border: 1px solid green;
            border-radius: 5%;
            padding: 10px;
            height: 300px;
            flex: 1;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .box:hover {
            border-color: darkgreen;
            background-color: limegreen;
        }
        </style>
        <div class='flex-container'>
            <div class='box'>
                <h6>Market Trends</h6>
                <p>Top Gainers, Top Losers, Indices of the days.</p>
            </div>
            <div class='box'>
                <h6>Stock Dashboard</h6>
                <p>Data visualization for different periods, returns, and fundamentals.</p>
            </div>
            <div class='box'>
                <h6>Analysis</h6>
                <p>Technical indicators, live data, stock predictions.</p>
            </div>
            <div class='box'>
                <h6>Watchlist</h6>
                <p>Create a watchlist and add stocks by sector.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_contact():
    st.subheader("Contact Us")
    
    # Path to the JSON file
DATA_FILE = 'contact_data.json'

# Function to save contact data to a JSON file
def save_contact_data(name, email, message):
    # Create the file if it doesn't exist
    if not os.path.isfile(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
    
    # Load existing data
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    # Append new contact data
    data.append({
        'name': name,
        'email': email,
        'message': message
    })
    
    # Save the updated data back to the file
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Function to display the contact section
def display_contact():
    st.subheader("Contact Us")
    
    # Styling the contact section
    st.markdown("""
    <style>
        .contact-container {
            background-color: #f9f9f9;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            margin: 0 auto;
        }
        .contact-container h3 {
            margin-bottom: 20px;
        }
        .contact-form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .contact-form input,
        .contact-form textarea {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
        }
        .contact-form textarea {
            resize: vertical;
            min-height: 100px;
        }
        .contact-form button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .contact-form button:hover {
            background-color: #45a049;
        }
    </style>
    """, unsafe_allow_html=True)

    # Contact form fields
    with st.form(key='contact_form'):
        st.write("We'd love to hear from you! Please fill out the form below and we'll get back to you as soon as possible.")
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        
        # Submit button
        submit_button = st.form_submit_button("Send Message")
        
        if submit_button:
            if name and email and message:
                save_contact_data(name, email, message)
                st.success(f"Thank you for your message, {name}! We will get back to you at {email} shortly.")
            else:
                st.error("Please fill out all fields before submitting.")

# Function to display the investment section
def display_investment():
    st.subheader("Investment Opportunities")

    # Styling for the investment section
    st.markdown("""
    <style>
        .investment-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
        }
        .investment-card {
            background-color: #f0f8ff; /* Light blue background */
            border: 1px solid #d1e0e0; /* Light grey border */
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            width: 300px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .investment-card:hover {
            transform: translateY(-10px);
            box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
        }
        .investment-card h4 {
            margin-top: 0;
            color: #007BFF; /* Bright blue */
        }
        .investment-card p {
            margin-bottom: 0;
            color: #333;
        }
        .investment-card a {
            text-decoration: none;
            color: #007BFF; /* Bright blue */
            font-weight: bold;
            transition: color 0.3s ease;
        }
        .investment-card a:hover {
            color: #0056b3; /* Darker blue */
        }
    </style>
    """, unsafe_allow_html=True)

    # Investment opportunities
    st.markdown("""
    <div class="investment-container">
        <div class="investment-card">
            <h4>Top Growth Stocks</h4>
            <p>Explore the stocks with the highest growth potential for the next quarter. Stay ahead of the market trends!</p>
            <a href="#">Learn More</a>
        </div>
        <div class="investment-card">
            <h4>Investment Strategies</h4>
            <p>Discover various investment strategies to optimize your portfolio and maximize returns.</p>
            <a href="#">Explore Strategies</a>
        </div>
        <div class="investment-card">
            <h4>Market Insights</h4>
            <p>Get detailed insights into current market trends and economic factors affecting your investments.</p>
            <a href="#">Read Insights</a>
        </div>
        <div class="investment-card">
            <h4>Beginner's Guide</h4>
            <p>New to investing? Check out our comprehensive guide to get started with the basics of investment.</p>
            <a href="#">Start Learning</a>
        </div>
    </div>
    """, unsafe_allow_html=True)


# Function to display the newsletter section
def display_newsletter():
    st.subheader("Subscribe to Our Newsletter")

    # Styling for the newsletter section
    st.markdown("""
    <style>
        .newsletter-container h3 {
            margin-bottom: 20px;
            color: #333;
        }
        .newsletter-form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .newsletter-form input[type="email"] {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
            width: 100%;
        }
        .newsletter-form button {
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .newsletter-form button:hover {
            background-color: #0056b3;
        }
        .newsletter-success {
            color: #28a745;
            font-weight: bold;
        }
        .newsletter-error {
            color: #dc3545;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    # Newsletter subscription form
    with st.form(key='newsletter_form', clear_on_submit=True):
        st.markdown('<div class="newsletter-container">', unsafe_allow_html=True)
        st.write("**Stay updated with the latest news and offers from StockAI.**")
        email = st.text_input("Enter your email address", placeholder="you@example.com")
        
        # Submit button
        submit_button = st.form_submit_button("Subscribe")
        
        if submit_button:
            if email:
                # Save email to a file or database (mocked here)
                st.markdown('<p class="newsletter-success">Thanks for subscribing! We will send updates to your email address.</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="newsletter-error">Please enter a valid email address.</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


# Function to display the "Follow Us" section
def display_footer():
    st.markdown("""
    <footer>
        <style>
            footer {
                background-color: #2c2c2c; /* Dark grey background */
                color: #e0e0e0; /* Light grey text color */
                padding: 40px 20px;
                text-align: center;
                font-family: 'Poppins', sans-serif;
            }
            .footer-content {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                max-width: 1200px;
                margin: 0 auto;
                gap: 30px;
            }
            .footer-section {
                flex: 1;
                min-width: 250px;
                margin-bottom: 20px;
            }
            .footer-section h4 {
                margin-bottom: 15px;
                color: #4CAF50; /* Green color for headings */
                font-size: 22px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            .footer-section a {
                color: #e0e0e0;
                display: block;
                margin-bottom: 10px;
                text-decoration: none;
                transition: color 0.3s ease;
            }
            .footer-section a:hover {
                color: #4CAF50;
            }
            .social-icons {
                display: flex;
                justify-content: center;
                gap: 25px;
                margin-top: 20px;
                flex-wrap: wrap;
            }
            .social-icons a {
                color: #e0e0e0;
                font-size: 15px; /* Larger icons for better visibility */
                transition: color 0.3s ease, transform 0.3s ease;
                text-decoration: none;
            }
            .social-icons a:hover {
                color: #4CAF50;
                transform: scale(1.2); /* Slightly enlarge on hover */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Add shadow effect */
            }
            .footer-bottom {
                margin-top: 20px;
                border-top: 1px solid #4CAF50;
                padding-top: 10px;
                font-size: 14px;
                color: #b0b0b0;
            }
            .footer-bottom a {
                color: #4CAF50;
                text-decoration: none;
                font-weight: bold;
            }
            .footer-bottom a:hover {
                color: #2e7d32;
            }
        </style>
        <div class="footer-content">
            <div class="footer-section">
                <h4>About Us</h4>
                <a href="#">Our Story</a>
                <a href="#">Team</a>
                <a href="#">Careers</a>
                <a href="#">Press</a>
            </div>
            <div class="footer-section">
                <h4>Support</h4>
                <a href="#">Help Center</a>
                <a href="#">Contact Us</a>
                <a href="#">FAQs</a>
                <a href="#">Live Chat</a>
            </div>
            <div class="footer-section">
                <h4>Legal</h4>
                <a href="#">Terms of Service</a>
                <a href="#">Privacy Policy</a>
                <a href="#">Cookie Policy</a>
                <a href="#">Disclaimer</a>
            </div>
            <div class="footer-section social-icons">
                <span>
                <h4>Follow Us</h4>
                <a href="#" aria-label="Facebook" title="Facebook"><i class="fab fa-facebook-f"></i></a>
                <a href="#" aria-label="Twitter" title="Twitter"><i class="fab fa-twitter"></i></a>
                <a href="#" aria-label="Instagram" title="Instagram"><i class="fab fa-instagram"></i></a>
                <a href="#" aria-label="LinkedIn" title="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
                <a href="#" aria-label="YouTube" title="YouTube"><i class="fab fa-youtube"></i></a>
                </span>
            </div>
        </div>
        <div class="footer-bottom">
            <p>© 2024 StockAI. All rights reserved. | <a href="#">Privacy Policy</a> | <a href="#">Terms of Service</a></p>
        </div>
    </footer>
    """, unsafe_allow_html=True)

    # icon libraries if not already included
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    """, unsafe_allow_html=True)


def main():
    # Import CSS links once here
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    """, unsafe_allow_html=True)
    
    display_header()
    display_marquee()
    display_about()
    display_investment()
    display_newsletter()
    display_contact()
    display_footer()

if __name__ == "__main__":
    main()

