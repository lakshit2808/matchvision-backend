import streamlit as st
from Auth.Login import login
from Auth.Register import register
from DBConnection import get_user_data, set_referral_code
from dotenv import load_dotenv, dotenv_values


# Load environment variables
load_dotenv()

INIT_CREDIT = dotenv_values(".env")["REGISTER_INIT_CREDIT"]
REFERRAL_CREDIT = dotenv_values(".env")["REFERRAL_CREDITS"]
FRIEND_REFERRAL_CREDITS = dotenv_values(".env")["FRIEND_REFERRAL_CREDITS"]

INIT_CREDIT = int(INIT_CREDIT)
REFERRAL_CREDIT = int(REFERRAL_CREDIT)
FRIEND_REFERRAL_CREDITS = int(FRIEND_REFERRAL_CREDITS)

st.set_page_config(page_title="MatchVision.AI")

def referral():
    email = st.session_state['email']
    data = get_user_data(email)

    ref_code = data['email'][:3]+data['phone_no'][-4:]
    set_referral_code(email, ref_code)
    if st.sidebar.button('Logout'):
        st.session_state['logged_in'] = False
        st.experimental_rerun()    
    st.title("Invite Your Friends and Earn Credits!")
    st.subheader("Share the love and get rewarded when your friends join us.")
    
    st.markdown("### You Earn")
    st.write(f"Get {REFERRAL_CREDIT} Credits for each friend who signs up.")
    
    st.markdown("### They Earn")
    st.write(f"Your friends get {FRIEND_REFERRAL_CREDITS} extra Credits. Summing {INIT_CREDIT} + {FRIEND_REFERRAL_CREDITS} = {INIT_CREDIT+FRIEND_REFERRAL_CREDITS} Credits")
    
    st.markdown("## How It Works")
    st.write("1. Share your unique code.")
    st.write("2. Your friend signs up using your code.")
    st.write("3. You both receive your credits once they complete their first registeration.")
    
    st.markdown("## Your Referral Link/Code")
    st.code(ref_code.upper())


if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    choice = st.sidebar.selectbox('Select an option', ['Login', 'Register'])
    
    if choice == 'Login':
        login()
    elif choice == 'Register':
        register()
else:
    referral()
