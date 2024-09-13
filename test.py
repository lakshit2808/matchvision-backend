articles = [
    "Manchester United has been on a winning streak, showing excellent teamwork in their recent matches.",
    "Chelsea's recent form has been inconsistent, with defensive errors costing them crucial points.",
    "Liverpool's attacking play has been unstoppable, but their defense has been shaky in the last few games.",
    "Arsenal's midfield dominance has helped them control the flow of the game and create many scoring opportunities.",
    "Tottenham's resilience has been impressive, but their attack has been inconsistent, leading to mixed results.",
    "Leicester City has shown great composure in high-pressure situations, particularly in their last match.",
    "Everton's strong defense has kept them in contention, though their offensive play has been lacking creativity.",
    "Aston Villa has struggled with injuries, which has affected their form and consistency on the pitch.",
    "West Ham United's attacking duo has been in great form, scoring multiple goals in recent matches.",
    "Wolves have been defensively solid but are struggling to convert their chances into goals.",
    "Brighton's young talent has shown great promise, though their lack of experience is evident in crucial moments.",
    "Crystal Palace's defensive organization has been impressive, but their counter-attacks have not been as sharp.",
    "Southampton's recent matches have been characterized by high-scoring affairs, with their defense looking vulnerable.",
    "Leeds United's high-press style has caused problems for many teams, but they struggle to maintain consistency.",
    "Newcastle United's solid midfield has helped them dominate possession, though they lack a clinical finisher.",
    "Burnley's physical style has been effective in breaking up play, but they lack creativity in the final third.",
    "Sheffield United's defensive approach has helped them secure points, but their attack has been toothless.",
    "Fulham's fluid passing game has been entertaining to watch, though their defense has been leaky at times.",
    "Brentford's pressing game has disrupted many teams, but they often struggle to convert their chances.",
    "Norwich City's young squad has shown great determination, but their lack of experience is proving costly.",
    "Watford's defensive errors have been a major issue, leading to multiple goals conceded in recent games.",
    "Bournemouth's quick counter-attacks have caught many teams off guard, though they struggle to maintain possession.",
    "Cardiff City's physical approach has been effective in the Championship, though they are prone to lapses in concentration.",
    "Middlesbrough's solid defense has been key to their recent run of form, but they need more from their forwards.",
    "Nottingham Forest's young attackers have been a bright spark, though their inexperience shows at crucial moments.",
    "Derby County's off-field issues have affected their on-field performances, leading to inconsistent results.",
    "Reading's organized defense has frustrated many opponents, though their attack has lacked creativity.",
    "Barnsley's pressing game has caused problems for many teams, but their defense has been vulnerable on the break.",
    "Blackburn Rovers' solid midfield has helped them control games, though their forwards have been wasteful in front of goal.",
    "Stoke City's physicality has been a key factor in their defensive solidity, but their attack has been toothless.",
    "Hull City's fast-paced attack has caught many teams off guard, but their defense has been shaky.",
    "Swansea City's passing game has been a joy to watch, though their defense has been vulnerable to set-pieces.",
    "Bristol City's young squad has shown great promise, but they need to be more clinical in front of goal.",
    "Preston North End's defensive organization has frustrated many teams, but they need more from their forwards.",
    "Luton Town's high-pressing game has caused problems for many teams, but their finishing has been inconsistent.",
    "Coventry City's midfield has been dominant, but their lack of a clinical striker has cost them points.",
    "Millwall's physicality has been effective in breaking up play, though they lack creativity in the final third.",
    "QPR's fluid passing game has been entertaining, but their defense has been leaky at times.",
    "West Brom's counter-attacking style has been effective, but they struggle to maintain possession.",
    "Huddersfield Town's solid defense has been key to their recent run of form, though they need more from their attackers.",
    "Birmingham City's defensive errors have been a major issue, leading to multiple goals conceded in recent games.",
    # Continue this pattern for up to 200 articles
]

# Define synthetic teams
team1 = "Manchester United"
team2 = "Chelsea"



import ollama
from time import time
import asyncio  # For parallel processing

start = time()

# Optimizing questions by keeping them concise
questions = [
    f"Based on the sentiment in the article: '{body[:100]}', which team is likely to win between {team1} and {team2}? Just give the team name or say NAN."
    for body in articles
]

# Prepare the prompts efficiently
prompts = [
    f"<s>[INST]\n<<SYS>>\n{question}\n{context[:200]}\n<</SYS>>\n\n{{user_prompt}}[/INST]"
    for question, context in zip(questions, articles)
]

# Async function to parallelize API requests for faster execution
async def fetch_response(prompt):
    return ollama.chat(model='llama3:8b', messages=[
        {
            'role': 'user',  
            'content': prompt,
        },
    ])['message']['content']

# Batch process the requests asynchronously
async def main():
    tasks = [fetch_response(prompt) for prompt in prompts]
    responses = await asyncio.gather(*tasks)
    return responses

# Running the main loop for asynchronous processing
responses = asyncio.run(main())

# Output the responses
print(responses)

end = time()

# Time taken for the entire process
print(f"Total time taken {end - start} seconds")




fireworks = "fw_3ZPU46vFghRs5vw6HpYKepqS"

from time import time
from fireworks.client import Fireworks

# Initialize the Fireworks client
client = Fireworks(api_key=fireworks)

start = time()

# Generate the questions for each article
questions = [
    f"Based on the sentiment in the article: '{body}', which team is likely to win between {team1} and {team2}? Just give the team name and don't give any reason, just give name of the team based on the view of author, if it's not understood by you just say NAN"
    for body in articles
]

# Combine the question and article to create a prompt
prompts = [
    f"<s>[INST]\n<<SYS>>\n{question}\n{context}\n<</SYS>>\n\n{{user_prompt}}[/INST]"
    for question, context in zip(questions, articles)
]

# Send prompts to the Fireworks client and get responses
responses = [
    client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="accounts/fireworks/models/llama-v3p1-8b-instruct",
    ).choices[0].message.content
    for prompt in prompts
]

print(responses)

end = time()

print(f"Total time taken: {end - start} seconds")
