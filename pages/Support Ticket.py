import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage
from dotenv import load_dotenv, dotenv_values

# Load environment variables
load_dotenv()

admin_email = dotenv_values(".env")["ADMIN_EMAIL"]
from_email = dotenv_values(".env")["FROM_EMAIL"]
app_pass = dotenv_values(".env")["GMAIL_APP_PASSWORD"]
smtp_server = dotenv_values(".env")["SMTP_SERVER"]
port = dotenv_values('.env')["SMTP_PORT"]

st.set_page_config(page_title="MatchVision.AI")

def send_email(to_email, subject, message):

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP(f"{smtp_server}", port )
        server.starttls()
        server.login(from_email, app_pass)
        msg = EmailMessage()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = 'Your OTP Code'
        msg.set_content(message)
        server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

# Streamlit app
st.title("Support Ticket")

st.markdown("Please fill out the form below to submit a support ticket. Our support team will get back to you as soon as possible.")

with st.form(key='support_ticket_form'):
    
    name = st.text_input("Name")
    email = st.text_input("Email")
    issue_type = st.selectbox("Issue Type", ["Technical Issue", "Billing Issue", "General Inquiry"])
    issue_description = st.text_area("Issue Description")

    submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        if name and email and issue_type and issue_description:
            # Create the email content
            subject = f"Support Ticket - {issue_type}"
            message = f"Name: {name}\nEmail: {email}\nIssue Type: {issue_type}\n\nIssue Description:\n{issue_description}"

            # Send the email
            if send_email(admin_email, subject, message):  # Update with your support email address
                st.success("Your support ticket has been submitted successfully.")
            else:
                st.error("There was an error submitting your support ticket. Please try again later.")
        else:
            st.error("Please fill in all the fields before submitting.")
