import streamlit as st
from socialmedia import RedditPredictor
from news import ArticleAnalyzer
from histmodel import FootballPrediction
from Baseball import BaseBall
from probcalc import combine_probabilities
from dotenv import load_dotenv, dotenv_values
import altair as alt
from DBConnection import get_credits, get_name, decrement_credits, prediction_storage
import pandas as pd
import time

load_dotenv()

api_key = dotenv_values(".env")["API_FOOTBALL_API_KEY"]
b_api_key = dotenv_values(".env")["BASEBALL_API_KEY"]
payment_url = dotenv_values(".env")["PAYMENT_URL"]

def display_card(bookmaker, odds_data):
    with st.expander(f"Bookmaker: {bookmaker}", expanded=True):
        for team, price in odds_data.items():
            st.markdown(f"**{team}:** {price}")

def Dashboard():
    """Main app functionality"""
    predict_status = True

    # User Info
    user_email = st.session_state['email']
    name = get_name(user_email)

    # Streamlit app setup
    st.title(f"Hey, {name}")
    st.title(f"Welcome to MatchVision.AI")
    # Credit Management
    credits = get_credits(user_email)
    st.write(f"## Available Credits: {credits}")
    st.write("Get In-Depth Match Insights for Only **5 Credits Per Prediction**")

    # Add More Credits
    st.link_button("Add More Credits", payment_url)
    
    # Highlight the features of the prediction model
    features = """
    # Welcome to the Match Prediction Console

    Step into the future of sports predictions, the ultimate tool for accurate match outcomes. Use advanced machine learning models, our app predicts sports match results by integrating Team Statistics, recent form of team, player performance, expert views, fans thoughts. Here’s how we do it:

    ### Highly Advance Prediction Models
    - **Calculating Match Outcomes**: Our sophisticated algorithms utilize Poisson Distribution, team statistics, recent form, and player performance to forecast match results.
    - **Generative AI**: Powered by LLAMA3 with 8 billion tokens, our system delivers superior predictive capabilities for understanding expert views.
    - **Sentiment Analysis**: By aggregating expert articles and public opinion, we provide a comprehensive prediction.

    ### Robust ETL Pipeline
    Our efficient ETL pipeline ensures seamless data fetching, cleaning, and loading, supporting accurate model training and prediction.

    ### Comprehensive Insights
    We combine probabilities from three different machine learning models:
    - **Fans View Model**: Analyzes comments from top posts to provide valuable insights.
    - **Machine Learning  Model**: Evaluates team statistics, recent form, and player performance.
    - **Expert View Model**: Evaluates multiple articles to aggregate their probability.
    - **Combined Probability**: Our advanced algorithm integrates all data for a final prediction.

    ### Visualization and Summarization
    - **Visual Outcomes**: View predictions from all models in an intuitive dashboard.
    - **Comment Summary**: Summarizes hundreds or thousands of comments into actionable insights.
    - **Article Summary**: Provides concise summaries of numerous expert articles.

    ## Your Opinion Matters!

    We continuously strive to improve our product and provide you with the best possible experience. Your feedback is invaluable to us, and we would love to hear from you!

    ### Submit Your Feedback and Earn 20 Credits!

    #### Why Participate?
    - **Help Us Improve**: Your insights will help us make our product even better.
    - **Earn Rewards**: Receive 20 credits as a token of our appreciation upon submitting your feedback.
    - **Be Heard**: Your suggestions and comments directly influence our development priorities.

    #### How to Participate?
    1. **Fill Out the Feedback Form**: Share your thoughts, experiences, and suggestions about our product.
    2. **Submit**: Simply submit the form and we'll take care of the rest.
    3. **Receive Your Credits**: After submission, 20 credits will be added to your account as a thank you.

    Experience the future of sports predictions and gain actionable insights with us. Join us today and be a part of our journey to revolutionize sports analytics!
    """
    if 'expanded' not in st.session_state:
        st.session_state.expanded = True

    # Function to toggle the expander state
    def toggle_expander():
        st.session_state.expanded = not st.session_state.expanded

    with st.expander("Transform Your Sports Analysis with MatchVision.AI", expanded=st.session_state.expanded):
        st.markdown(features)

    # Sidebar inputs
    credits = get_credits(user_email)
    st.sidebar.header('Configure Inputs')
    if credits != 0:
        config_status = False
    else:
        st.markdown(
            """
            <div style="background-color: #f8d7da; color: #721c24;margin:15px ; padding: 15px; border: 1px solid #f5c6cb; border-radius: 4px;">
                <strong>Attention:</strong> Your current credits are finished. Please Add more credits now to enable input configurations!
            </div></hr>
            """,
            unsafe_allow_html=True
        )        
        config_status = True
    sports = st.sidebar.selectbox('Select Sports', ['Baseball']) # Football

    home_team = st.sidebar.text_input('Home Team', '', disabled=config_status)
    away_team = st.sidebar.text_input('Away Team', '',disabled=config_status)

    date_of_match = st.sidebar.date_input('Date of Match', key='Date', disabled=config_status)
    total_articles = st.sidebar.number_input(
        'Total Articles', min_value=1, max_value=15, value=5, disabled=config_status
    )
    num_posts = st.sidebar.number_input(
        'Number of Posts', min_value=1, max_value=10, value=3, disabled=config_status
    )
    bm_check_list = ["No", "Yes"]
    bm_check = st.sidebar.selectbox('Want to check odds from different bookmakers?', bm_check_list)    
    if bm_check == "Yes":
        # Sidebar for selecting region
        regions = ["us", "us2", "uk", "au", "eu", "all available"]
        selected_region = st.sidebar.selectbox('Select Bookmaker Region', regions)


    if home_team and away_team:
        predict_status = False
    if st.sidebar.button("Predict", disabled = predict_status):
        start = time.time()
        # st.session_state.clear()
        if st.session_state.expanded:
            toggle_expander()
        total_steps = 5  # Total number of processes
        progress = [0]   # Use a list to hold the progress value

        if sports == "Football":
            football_prediction = FootballPrediction(api_key)
        baseball_prediction = BaseBall(b_api_key, home_team, away_team, sports)
        predictor = RedditPredictor()
        analyzer = ArticleAnalyzer(home_team, away_team, total_articles)

        def update_progress():
            progress[0] += 1
            st.write(f"Progress: {progress[0]}/{total_steps} completed")

        def chart(ht_prob, at_prob):
            data = {
                'Team': [home_team, away_team],
                'Probability': [ht_prob, at_prob]
            }
            df = pd.DataFrame(data)
            # Display the bar chart
            chart = alt.Chart(df).mark_bar(size=30).encode(
                x=alt.X('Team', axis=alt.Axis(title='')),
                y=alt.Y('Probability', scale=alt.Scale(domain=[0, 1])),
                color=alt.Color('Team', scale=alt.Scale(range=['#1f77b4', '#ff7f0e']))
            ).properties(
                width=300,
                height=200
            )
            return st.altair_chart(chart, use_container_width=True)     

        try:
            with st.spinner("Calculating Match Outcome Based on Poisson Distribution, Team Statistics, Recent Form, and Player Performance..."):
                if sports == 'Football':
                    historical_prediction = football_prediction.get_match_prediction(home_team, away_team, date_of_match)
                else:
                    historical_prediction = baseball_prediction.fetch_h2h_odds()
                st.success("Historical performance prediction complete!")
                update_progress()
        except Exception as e:
            st.error(f"Error Making Performance Prediction: {e}")
            st.session_state['logged_in']
            # st.stop() 
            return

        try:
            with st.spinner("Analyzing Articles..."):
                article_urls = analyzer.fetch_article_links(sports)
                if len(article_urls) == 0:
                    st.error("No articles found. Try Different Game")
                    return
                article_contents = analyzer.get_full_article_content(article_urls)
                article_prediction = analyzer.expert_view_prediction(article_contents)
                st.success("Article analysis complete!")
                update_progress()
        except Exception as e:
            st.error(f"Error analyzing articles: {e}")
            # st.stop() 
            return    
        try:
            with st.spinner("Summarizing Articles..."):
                article_summary = analyzer.summarize_articles(article_contents, home_team, away_team)
                st.success("Article summarizing completed!")
                update_progress()
        except Exception as e:
            st.error(f"Error summarizing articles: {e}")
            # st.stop() 
            return    

        try:
            reddit_query = f"{home_team} vs {away_team} {sports} match prediction reddit"
            reddit_urls = predictor.scrape_google_search_urls(reddit_query, num_results=num_posts)
            reddit_data = predictor.fetch_reddit_post_comments(reddit_urls)
            with st.spinner(f"Analyzing {len(reddit_data)} Reddit Comments..."):
                reddit_prediction = predictor.expert_view_prediction(home_team, away_team, reddit_data)
                st.success("Reddit analysis complete!")
                update_progress()
        except Exception as e:
            st.error(f"Error analyzing reddit comments: {e}")
            # st.stop() 
            return    
        try:

            with st.spinner(f"Summarizing {len(reddit_data)} Reddit Comments..."):
                reddit_summary = predictor.summarize_comments(reddit_data, home_team,away_team)
                st.success("Comment summarizing completed!")
                update_progress()
        except Exception as e:
            st.error(f"Error summarizing reddit comments: {e}")
            # st.stop() 
            return    

        st.write("Process completed!")

        if bm_check == "Yes":
            try:
                with st.spinner("Gathering Bookmakers..."):
                    bookmaker_odds = baseball_prediction.bookmaker_odds()
                    data = bookmaker_odds
                    
                    if len(data) == 0:
                        st.error("No data found from bookmakers.")
                        return
                    
                    st.success("Bookmakers fetched!")
                    update_progress()

            except Exception as e:
                st.error(f"Error gathering bookmakers: {e}")
                # st.stop() 
                return
     

        st.subheader('Result Summary')
        # Display results
        try:
            # Credit Subtraction
            decrement_credits(user_email)

            st.markdown("<h4>Article Prediction:</h4>", unsafe_allow_html=True)
            chart(round(article_prediction[1],2), round(article_prediction[2],2))
            with st.expander("Insightful Articles Overview", expanded=True):
                st.write(article_summary)

            st.markdown("<h4>Comment Prediction:</h4>", unsafe_allow_html=True)
            chart(round(reddit_prediction[1],2), round(reddit_prediction[2],2))
            with st.expander("Insightful Comment Overview", expanded=True):
                st.write(reddit_summary)            

            st.markdown("<h4>Historical Prediction:</h4>", unsafe_allow_html=True)
            chart(historical_prediction[0], historical_prediction[1])

            # Combine predictions
            combined_prob = combine_probabilities(article_prediction[1:], reddit_prediction[1:], historical_prediction)
            if combined_prob == -1:
                st.write("Draw")
            else:
                st.markdown(f"<h4>Combined Probability for {home_team}: {combined_prob[0]:.2f}</h4>", unsafe_allow_html=True)
                st.markdown(f"<h4>Combined Probability for {away_team}: {combined_prob[1]:.2f}</h4>", unsafe_allow_html=True)

                chart(round(combined_prob[0],2), round(combined_prob[1],2))


            prediction_data = {
                "sports": sports,
                "team_1": home_team,
                "team_2": away_team,
                "date_of_match": date_of_match,
                "total_articles": total_articles,
                "no_of_posts": num_posts,
                "article_summary": article_summary,
                "article_prediction": article_prediction[1:],
                "comment_summary": reddit_summary,
                "comment_prediction": reddit_prediction[1:],
                "hist_prediction": historical_prediction,
                "combined_prediction": combined_prob}

            if bm_check == "Yes":
                # Filter options
                st.subheader('Odds from Different Bookmakers for both teams in {selected_region} region:')

                # Filter data based on user selection
                if selected_region == "all available":
                    filtered_data = [item for item in data]
                else:    
                    filtered_data = [item for item in data if item['region'] == selected_region]
                # Calculate the number of pairs needed
                num_cards = len(filtered_data)
                num_pairs = (num_cards + 1) // 2  # +1 to account for odd number of cards

                for i in range(num_pairs):
                    with st.container():
                        col1, col2 = st.columns(2)
                        
                        # Card 1
                        if 2 * i < num_cards:
                            item1 = filtered_data[2 * i]
                            bookmaker1 = item1['bookmaker']
                            odds_data1 = {outcome['name']: outcome['price'] for outcome in item1['odds']}
                            
                            with col1:
                                display_card(bookmaker1, odds_data1)
                        
                        # Card 2
                        if 2 * i + 1 < num_cards:
                            item2 = filtered_data[2 * i + 1]
                            bookmaker2 = item2['bookmaker']
                            odds_data2 = {outcome['name']: outcome['price'] for outcome in item2['odds']}
                            
                            with col2:
                                display_card(bookmaker2, odds_data2)  

            print("Storing Prediction...")
            prediction_storage(prediction_data)
            print("Prediction Stored!")
            end = time.time()
            st.write(f"Time taken: {end - start} seconds")
            
            
        except Exception as e:
            st.error(f"Error displaying or combining predictions: {e}")

    else:
        st.sidebar.write("*NOTE:-* Please fill in all input fields to enable the **Predict** button.")