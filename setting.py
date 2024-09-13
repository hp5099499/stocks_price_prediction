import streamlit as st
from pymongo import MongoClient
import re
import os
from translate import Translator

# Initialize MongoDB connection
client = MongoClient("mongodb+srv://himanshu:himanshu@user-database.tm5go.mongodb.net/?retryWrites=true&w=majority&appName=user-database")
db = client["user_database"]
users_collection = db["users"]
support_collection = db["support_requests"]

def translate_text(text, dest_lang):
    try:
        translator = Translator(to_lang=dest_lang)
        translated = translator.translate(text)
        return translated
    except Exception as e:
        st.error(f"Error in translation: {e}")
        return text

def language_selector():
    lang_options = {
        "English": "en",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Chinese (Simplified)": "zh",
        "Chinese (Traditional)": "zh-tw",
        "Hindi": "hi",
        "Tamil": "ta",
        "Telugu": "te",
        "Bengali": "bn",
        "Kannada": "kn",
        "Marathi": "mr",
        "Gujarati": "gu",
        "Malayalam": "ml",
        "Punjabi": "pa",
        "Arabic": "ar",
        "Dutch": "nl",
        "Greek": "el",
        "Hebrew": "he",
        "Hungarian": "hu",
        "Indonesian": "id",
        "Italian": "it",
        "Japanese": "ja",
        "Korean": "ko",
        "Malay": "ms",
        "Norwegian": "no",
        "Polish": "pl",
        "Portuguese": "pt",
        "Romanian": "ro",
        "Russian": "ru",
        "Serbian": "sr",
        "Swedish": "sv",
        "Thai": "th",
        "Turkish": "tr",
        "Ukrainian": "uk",
        "Vietnamese": "vi",
    }
    lang_code = st.selectbox("Select Language", list(lang_options.keys()))
    dest_lang = lang_options[lang_code]
    return dest_lang

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_mobile(mobile):
    return re.match(r"^\d{10}$", mobile)

def is_strong_password(password):
    return (
        len(password) >= 8 and
        re.search(r'[A-Za-z]', password) and
        re.search(r'[0-9]', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    )

def save_user_data(username, user_data):
    """Save or update user details in MongoDB."""
    users_collection.update_one(
        {"username": username},
        {"$set": user_data},
        upsert=True
    )
    st.success("User data saved successfully!")

def save_problem_report(report_data, username):
    """Save or update a problem report for a user in MongoDB."""
    users_collection.update_one(
        {"username": username},
        {"$push": {"problem_reports": report_data}},  # Use $push to add to problem_reports array
        upsert=True
    )
    st.success("Your report has been submitted successfully!")

def save_support_request(request_data):
    """Save support request to MongoDB."""
    support_collection.insert_one(request_data)
    st.success("Your support request has been submitted successfully!")

def report_problem(lang):
    st.subheader(translate_text("Report a Problem", lang))
    st.write(translate_text("Please provide detailed information about the issue you are experiencing. This will help us assist you more effectively.", lang))
    
    category = st.selectbox(translate_text("Select Problem Category", lang), ["Technical Issue", "Account Issue", "Billing Issue", "Feature Request", "Other"])
    problem_description = st.text_area(translate_text("Describe your problem or feedback here:", lang), height=150)
    uploaded_file = st.file_uploader(translate_text("Upload a screenshot or relevant file (optional):", lang), type=["png", "jpg", "jpeg", "pdf"])
    
    if st.button(translate_text("Submit Report", lang)):
        if problem_description:
            report_data = {
                "username": st.session_state["username"],
                "category": category,
                "description": problem_description,
                "attachment": None
            }
            if uploaded_file:
                attachments_dir = "attachments"
                if not os.path.exists(attachments_dir):
                    os.makedirs(attachments_dir)
                file_path = os.path.join(attachments_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                report_data["attachment"] = file_path
                st.success(translate_text("File uploaded successfully! ✅", lang))
            save_problem_report(report_data, st.session_state["username"])
        else:
            st.error(translate_text("Please describe your problem before submitting.", lang))

def change_password(lang):
    st.subheader(translate_text("Change Password", lang))
    
    password_col1, password_col2 = st.columns([3, 1])
    
    with password_col1:
        current_password = st.text_input(translate_text("Current Password", lang), type="password")
        new_password = st.text_input(translate_text("New Password", lang), type="password")
        confirm_password = st.text_input(translate_text("Confirm New Password", lang), type="password")
    
    with password_col2:
        if new_password:
            if is_strong_password(new_password):
                st.markdown(f"{translate_text('Password Strength:', lang)} Strong**", unsafe_allow_html=True)
            else:
                st.markdown(f"{translate_text('Password Strength:', lang)} Weak**", unsafe_allow_html=True)
    
    if st.button(translate_text("Change Password", lang)):
        if new_password == confirm_password:
            if is_strong_password(new_password):
                # Update the password in the database here
                # For security reasons, you would normally hash the password before storing it
                st.success(translate_text("Password Changed Successfully! 🔒", lang))
            else:
                st.error(translate_text("New Password is not strong enough! ❌", lang))
        else:
            st.error(translate_text("New Password and Confirm Password do not match! ❌", lang))

def help_and_support(lang):
    st.subheader(translate_text("Help and Support", lang))
    st.write(translate_text("Welcome to the Help and Support section. Here you can find resources to assist you:", lang))
    
    st.write(translate_text("*1. Frequently Asked Questions (FAQ):*", lang))
    st.write(translate_text("   - What is this application?", lang))
    st.write(translate_text("   - How do I reset my password?", lang))
    st.write(translate_text("   - How do I contact support?", lang))
    
    st.write(translate_text("*2. Contact Support:*", lang))
    st.write(translate_text("   - Email: support@example.com", lang))
    st.write(translate_text("   - Phone: +1-800-123-4567", lang))
    st.write(translate_text("   - Support Hours: Mon-Fri, 9 AM - 5 PM (EST)", lang))
    
    st.write(translate_text("*3. User Guides:*", lang))
    st.write(translate_text("   - [User Guide for Beginners](https://example.com/user-guide)", lang))
    st.write(translate_text("   - [Advanced Features Guide](https://example.com/advanced-guide)", lang))
    
    st.write(translate_text("*4. Community Forums:*", lang))
    st.write(translate_text("   - [Join the Community Forum](https://example.com/forum)", lang))
    
    st.write(translate_text("*5. Support Form:*", lang))
    st.write(translate_text("If you have a specific issue or request, please fill out the form below.", lang))
    
    with st.form(key='support_form'):
        name = st.text_input(translate_text("Your Name", lang))
        email = st.text_input(translate_text("Your Email", lang))
        subject = st.text_input(translate_text("Subject", lang))
        message = st.text_area(translate_text("Message", lang), height=150)
        submit_button = st.form_submit_button(translate_text("Submit", lang))
        
        if submit_button:
            if name and email and subject and message:
                request_data = {
                    "name": name,
                    "email": email,
                    "subject": subject,
                    "message": message
                }
                save_support_request(request_data)
            else:
                st.error(translate_text("Please fill out all required fields before submitting.", lang))

def user_details(lang):
    st.subheader(translate_text("User Details", lang))
    
    # Using columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input(translate_text("Name", lang), max_chars=50)
        dob = st.date_input(translate_text("Date of Birth", lang))
        gender = st.selectbox(translate_text("Gender", lang), ["Male", "Female", "Other"])
    
    with col2:
        mobile = st.text_input(translate_text("Mobile Number", lang), max_chars=10)
        marital_status = st.selectbox(translate_text("Marital Status", lang), ["Single", "Married", "Divorced", "Widowed"])
        email = st.text_input(translate_text("Email", lang))
    
    # Validation messages
    if st.button(translate_text("Save Details", lang)):
        errors = []
        if not name:
            errors.append(translate_text("Name is required.", lang))
        if not email or not is_valid_email(email):
            errors.append(translate_text("A valid email is required.", lang))
        if not mobile or not is_valid_mobile(mobile):
            errors.append(translate_text("A valid 10-digit mobile number is required.", lang))
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            user_data = {
                "name": name,
                "date_of_birth": str(dob),
                "gender": gender,
                "mobile": mobile,
                "marital_status": marital_status,
                "email": email
            }
            save_user_data(st.session_state["username"], user_data)

def main():
    if "username" not in st.session_state:
        st.warning("Please log in first.")
        st.stop()

    lang = language_selector()

    # Title and Sidebar Navigation
    st.markdown(translate_text("<div class='header'>Settings", lang),unsafe_allow_html=True)
    
    menu = [
        translate_text("User Details", lang),
        translate_text("Change Password", lang),
        translate_text("Report a Problem", lang),
        translate_text("Help and Support", lang)
    ]
    choice = st.sidebar.selectbox(translate_text("Select Option", lang), menu)
    
    if choice == translate_text("User Details", lang):
        user_details(lang)
    elif choice == translate_text("Change Password", lang):
        change_password(lang)
    elif choice == translate_text("Report a Problem", lang):
        report_problem(lang)
    elif choice == translate_text("Help and Support", lang):
        help_and_support(lang)

if __name__ == '__main__':
    main()

