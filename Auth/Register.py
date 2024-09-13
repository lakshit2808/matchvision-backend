import streamlit as st
from twilio.rest import Client
import re
import pyotp
from Auth.Login import generate_otp, verify_otp
from DBConnection import register_user, referal_code_check, ref_increment_credits, set_referral, increment_credits
from dotenv import load_dotenv, dotenv_values

# Load environment variables
load_dotenv()

INIT_CREDIT = dotenv_values(".env")["REGISTER_INIT_CREDIT"]
TWILIO_SID = dotenv_values(".env")["TWILIO_SID"]
TWILIO_AUTH_TOKEN = dotenv_values(".env")["TWILIO_AUTH_TOKEN"]
TWILIO_MOBILE_NO = dotenv_values(".env")["TWILIO_MOBILE_NO"]
MOBILE_OTP_SEC = dotenv_values(".env")["MOBILE_OTP_SECRET"]
FRIEND_REFERRAL_CREDITS = dotenv_values(".env")["FRIEND_REFERRAL_CREDITS"]

INIT_CREDIT = int(INIT_CREDIT)
FRIEND_REFERRAL_CREDITS = int(FRIEND_REFERRAL_CREDITS)

def send_mobile_otp(mob_nmbr_with_cc):
    try:
        totp = pyotp.TOTP(MOBILE_OTP_SEC, interval = 300)
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        otp = totp.now()    

        msg = client.messages.create(
            from_ = TWILIO_MOBILE_NO,
            to = f"{mob_nmbr_with_cc}",
            body = f"OTP is {otp} for Registeration at MatchVision.AI. Do not share OTP for security reasons"
        )
        return otp
    except:
         return False
    
def verify_mobile_otp(otp_input):
    """Verify the provided OTP."""
    totp = pyotp.TOTP(MOBILE_OTP_SEC, interval= 300)

    return totp.verify(otp_input)    
    

def validate_phone_number(phone_number):
    # Simple regex for phone number validation
    pattern = re.compile(r'^\+?[1-9]\d{1,14}$')
    return pattern.match(phone_number)
def validate_email(email):
    # Simple regex for email validation
    pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return pattern.match(email)

def register():
    """Handle user registration"""
    st.header('Register')
    name = st.text_input("Name")
    phone_no = st.text_input("Phone", placeholder="+11234567890")
    if phone_no:
        if not validate_phone_number(phone_no):
            st.error('Invalid phone number. Please enter a valid phone number.')
    email = st.text_input('Email')
    if email:
        if not validate_email(email):
            st.error('Invalid Email. Please enter a valid email.')    
    referral_code = st.text_input("Referral Code").lower()

    if st.button('Send OTP'):
        otp = generate_otp(email)
        # m_otp = send_mobile_otp(phone_no) Mobile_OTP _1
        st.session_state['otp'] = otp
        # st.session_state['m_otp'] = m_otp Mobile_OTP _2
        st.session_state['email'] = email
        st.session_state['otp_sent'] = True
        # st.success('OTP has been sent to your email. Please check your inbox.')    

    if st.session_state.get('otp_sent'):
        otp_input = st.text_input('Enter Email OTP', '')
        # pn_otp_input = st.text_input('Enter Phone OTP', '') Mobile_OTP _3
        if st.button('Verify and Register'):
            # if verify_otp(otp_input) and verify_mobile_otp(pn_otp_input) and email and phone_no: Mobile_OTP _4
            if verify_otp(otp_input) and email and phone_no:
                if referral_code == "":
                    if register_user(name, phone_no, email, INIT_CREDIT):
                        st.success('OTP verified successfully! You are now Registered. You can Now Proceed with Login')
                    else:
                        st.error('User already exists. Please choose to login instead of Registering.')
                else:
                    if register_user(name, phone_no, email, INIT_CREDIT):
                        if referal_code_check(referral_code, st):
                            ref_increment_credits(referral_code)
                            set_referral(email, referral_code)
                            increment_credits(email, FRIEND_REFERRAL_CREDITS)
                            st.success(f'Referral code is valid. You have been credited with {FRIEND_REFERRAL_CREDITS} extra credits.')
                            st.success('OTP verified successfully! You are now Registered. You can Now Proceed with Login')
                        st.experimental_rerun()
                    else:
                        st.error('User already exists. Please choose to login instead of Registering.')
            else:
                st.error('Invalid OTP. Please try again. Or Regenerate the OTP.')                       
    
