import streamlit as st

st.set_page_config(page_title="MatchVision.AI")

# Set the title of the page
st.title("FAQ: MatchVision.AI")


# General Information section
with st.expander("General Information"):
    st.subheader("Q1: What is the MatchVision.AI?")
    st.write("A: The MatchVision.AI is an advanced tool for predicting sports match outcomes. Using sophisticated machine learning models, the app integrates team statistics, recent form, player performance, expert views, and fan opinions to provide accurate match predictions.")

    st.subheader("Q2: How many credits do I have available?")
    st.write("A: You can view your available credits under dashboard or accounts page.")

    st.subheader("Q3: How many credits does each prediction cost?")
    st.write("A: Each prediction costs only 5 credits.")

# Prediction Models section
with st.expander("Prediction Models"):
    st.subheader("Q4: How does the MatchVision.AI predict match outcomes?")
    st.write("A: Our system utilizes advanced algorithms, including Poisson Distribution, to analyze team statistics, recent form, and player performance. It also employs Generative AI powered by LLAMA3 with 8 billion tokens to understand expert views and perform sentiment analysis on aggregated expert articles and public opinion.")

    st.subheader("Q5: What models are used in the prediction process?")
    st.write("""
    A: We use three main models:
    - **Fans View Model:** Analyzes comments from top posts to provide insights.
    - **Machine Learning Model:** Evaluates team statistics, recent form, and player performance.
    - **Expert View Model:** Aggregates probabilities from multiple expert articles.
    """)

    st.subheader("Q6: How is the final prediction calculated?")
    st.write("A: Our advanced algorithm combines probabilities from the Fans View Model, Machine Learning Model, and Expert View Model to generate a final prediction.")

# Data Processing section
with st.expander("Data Processing"):
    st.subheader("Q7: How does the ETL pipeline support the prediction process?")
    st.write("A: Our robust ETL (Extract, Transform, Load) pipeline ensures efficient data fetching, cleaning, and loading, which supports accurate model training and prediction.")

# Insights and Visualization section
with st.expander("Insights and Visualization"):
    st.subheader("Q8: What insights are provided by the MatchVision.AI?")
    st.write("A: The console offers comprehensive insights, including visual outcomes from all models, summaries of comments, and concise summaries of expert articles.")

    st.subheader("Q9: How can I view the predictions?")
    st.write("A: Predictions can be viewed in an intuitive dashboard that displays visual outcomes from all models.")

# Feedback and Credits section
with st.expander("Feedback and Credits"):
    st.subheader("Q10: How can I provide feedback?")
    st.write("A: You can fill out our feedback form to share your thoughts, experiences, and suggestions about our product.")

    st.subheader("Q11: What rewards do I get for providing feedback?")
    st.write("A: Upon submitting your feedback, you will earn 20 credits as a token of our appreciation.")

    st.subheader("Q12: Why should I participate in providing feedback?")
    st.write("A: Your insights help us improve our product. Additionally, you'll earn rewards and have your suggestions directly influence our development priorities.")

# Referral Program section
with st.expander("Referral Program"):
    st.subheader("Q13: How can I earn credits by inviting friends?")
    st.write("A: You can share your unique referral code with friends. When they sign up using your code, you earn 10 credits, and they earn 10 extra credits.")

    st.subheader("Q14: What is my referral code?")
    st.write("A: Your referral code is present in Referral program page.")

    st.subheader("Q15: How does the referral process work?")
    st.write("A: Share your unique code with friends. When they sign up using your code, you both receive your credits once they complete their first registration.")

# Inputs and Predictions section
with st.expander("Inputs and Predictions"):
    st.subheader("Q16: What information do I need to provide for predictions?")
    st.write("A: You need to fill in the home team, away team, date of the match, total number of articles, and number of posts.")

    st.subheader("Q17: What should I do if the team name is not recognized?")
    st.write('A: If the team name is not recognized, try different variations of the team name. For example, instead of "Egypt vs Paraguay," try "Egypt U23 vs Paraguay U23." Make sure the first letter is always uppercase. The names on Google match usually work.')

    st.subheader("Q18: What should I do if no fixture is available on a particular date?")
    st.write("A: If no fixture is available on the specific date, try one day before or after the date on Google.")

# Contact Us section
with st.expander("Contact Us"):
    st.subheader("Q19: How can I get in touch with customer support?")
    st.write("A: If you need assistance or have any questions, please contact our support team through the Support Ticket page on our app.")
