import streamlit as st
from PIL import Image
import io
import base64
import json
import os

# Function to save user data to JSON
def save_user_data(username, profile_image):
    if not os.path.exists('users.json'):
        with open('users.json', 'w') as f:
            json.dump({}, f)

    with open('users.json', 'r') as f:
        users = json.load(f)

    users[username] = {'profile_image': profile_image}

    with open('users.json', 'w') as f:
        json.dump(users, f)

# Function to handle the sidebar display
def display():
    # Load and encode logo image
    logo_path = "logo.jpg"  # Replace with your logo image file path
    logo_image = Image.open(logo_path)
    
    buffered = io.BytesIO()
    logo_image.save(buffered, format="PNG")
    logo_img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # Sidebar with title and logo
    st.sidebar.markdown(f"""
        <style>
            .sidebar-title {{
                display: flex;
                text-align:center;
                margin-left:15%;
            }}
            .sidebar-logo {{
                margin-top:-100px;
                width: 100px;
                height: 100px;
            
                
            }}
            .title-text {{
                font-size: 24px;
                font-weight: bold;
                margin-left:15%;
    
            }}
        </style>
        <div class="sidebar-title">
            <img src="data:image/png;base64,{logo_img_str}" class="sidebar-logo" /></div>
            <div class="title-text">StockAi</div>
        
    """, unsafe_allow_html=True)
    
    # Add login functionality
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.sidebar.header("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        
        # Simple login check (replace with your actual authentication logic)
        if st.sidebar.button("Login"):
            if username == "user" and password == "pass":  # Replace with your actual login check
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.uploaded = False
                st.sidebar.success("Login successful!")
            else:
                st.sidebar.error("Invalid credentials")
        
        st.stop()  # Stop further execution if not logged in

    # Rest of the sidebar content for logged-in users
    st.sidebar.markdown("<div class='header'>Profile</div>",unsafe_allow_html=True)
    
    if 'uploaded' not in st.session_state:
        st.session_state.uploaded = False
    if 'username' not in st.session_state:
        st.session_state.username = 'John Doe'  # Default username; replace as needed
    
    if not st.session_state.uploaded:
        uploaded_file = st.sidebar.file_uploader("Upload a profile picture", type=["jpg", "jpeg", "png"])
    
        if uploaded_file is not None:
            st.session_state.uploaded = True
            st.session_state.uploaded_file = uploaded_file
            profile_image = Image.open(uploaded_file)
            
            # Convert the image to base64
            buffered = io.BytesIO()
            profile_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Save user data
            save_user_data(st.session_state.username, img_str)
    else:
        profile_image = Image.open(st.session_state.uploaded_file)
        buffered = io.BytesIO()
        profile_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
    
    if not st.session_state.uploaded:
        profile_image = Image.open("profile.jpg")  # Replace with your default image file path
    
    # Convert the image to a base64 string
    buffered = io.BytesIO()
    profile_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # Custom CSS for profile section
    profile_css = f"""
        <style>
            .profile-content {{
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
            }}
            .circular-image {{
                width: 150px;
                height: 150px;
                border-radius: 50%;
                background-image: url(data:image/png;base64,{img_str});
                background-size: cover;
                margin-bottom: 10px;
            }}
        </style>
        <div class="profile-content">
            <div class="circular-image"></div>
        </div>
    """
    
    # Inject the CSS and HTML for the profile section
    st.sidebar.markdown(profile_css, unsafe_allow_html=True)
    
    # Add the logout button in the center of the sidebar
    

# Run the display function
if __name__ == "__main__":
    display()
