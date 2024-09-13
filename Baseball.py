
import requests


class BaseBall:
    def __init__(self, api_key, home_team, away_team, sports, regions='us'):
        self.api_key = api_key
        self.home_team = home_team
        self.away_team = away_team
        self.regions = regions
        self.sports = sports
        self.base_url = "https://api.the-odds-api.com/v4/sports/{league_code}/odds/"

    def get_league_code(self):
        url = "https://api.the-odds-api.com/v4/sports"
        params = {
            "apiKey": self.api_key,
        }
        response = requests.get(url, params=params).json()  
        leagues_code = []
        for code in response:
            if self.sports == code['group']:
                leagues_code.append(code['key'])
        return leagues_code

    def get_odds(self,league_code, regions = None):
        url = self.base_url.format(league_code=league_code)
        if regions is None:
            params = {
                'apiKey': self.api_key,
                'regions': self.regions
            }
            
        else:
            params = {
                'apiKey': self.api_key,
                'regions': regions
            }
        response = requests.get(url, params=params)
        return response.json()

    def fetch_h2h_odds(self):
        league_codes = self.get_league_code()
        for code in league_codes:
            res = self.get_odds(code)
            h2h_odds = []
            for r in res:
                if r["home_team"] == self.home_team or r["away_team"] == self.away_team:
                    for b in r["bookmakers"][:1]:
                        for m in b['markets']:
                            for o in m['outcomes']:
                                if o['name'] == self.home_team:
                                    h2h_odds.insert(0, o['price'])  # Insert at the beginning of the list
                                else:
                                    h2h_odds.append(o['price'])  # Append to the end of the list

        
            if len(h2h_odds) != 0 and len(h2h_odds) >= 2:
                # Calculate implied probabilities
                implied_probabilities = [(1/odds) for odds in h2h_odds]
                # Normalize probabilities to sum to 100%
                total_prob = sum(implied_probabilities)
                normalized_probabilities = [(prob / total_prob) for prob in implied_probabilities]
                
                h_win = round(normalized_probabilities[0], 2)
                a_win = round(normalized_probabilities[1], 2)
                return h_win, a_win
            
    def bookmaker_odds(self):
        league_codes = self.get_league_code()
        all_bookmaker_data = []  # Initialize as a list to store multiple bookmakers' data

        regions = ["us", "us2", "uk", "au", "eu"]
        
        for code in league_codes:
            # Fetch odds data for all regions at once if possible
            region_results = [self.get_odds(code, reg) for reg in regions]
            for reg, res in zip(regions, region_results):
                for r in res:
                    if r["home_team"] == self.home_team or r["away_team"] == self.away_team:
                        for b in r["bookmakers"]:
                            bookmaker_data = {
                                "region": reg,
                                "bookmaker": b['title'],
                                "odds": []
                            }
                            for m in b['markets']:
                                # Collect all outcomes in one step
                                outcomes = [
                                    {"name": o['name'], "price": o['price']}
                                    for o in m['outcomes']
                                ]
                                bookmaker_data["odds"].extend(outcomes)
                            
                            all_bookmaker_data.append(bookmaker_data)
        
        return all_bookmaker_data





# Example usage:
# api_key = "efb663a4e0b134f9560784c5ee3c7cb1"
# home_team = "Detroit Tigers"
# away_team = "Colorado Rockies"
# sports = "Baseball"

# odds_api = BaseBall(api_key, home_team, away_team, sports)
# odds = odds_api.fetch_h2h_odds()
# print(odds)
# SAMPLE OUTPUT >> (61.04, 38.96)

# bookmaker_odds = odds_api.bookmaker_odds()
# print(bookmaker_odds)







# import requests
# from time import sleep
# from probcalc import combine_probabilities

# delay = 0.5

# api_key = "69e9ab5f5c6b12f89c5a06cc50b3b106"
# headers = {'x-rapidapi-key': api_key}


# class BaseBall:

#     def __init__(self, api_key, team_1, team_2):
#         self.api_key = api_key
#         self.team_1 = team_1
#         self.team_2 = team_2
#         self.headers = {'x-rapidapi-key': api_key}
#         self.base_url = "https://v1.baseball.api-sports.io"
#         self.delay = 0.5

#     def get_team_id(self, name):
#         url = f"{self.base_url}/teams?name={name}"
#         response = requests.get(url, headers=self.headers)

#         data = response.json().get('response', [{}])

#         if len(data) != 0:
#             return data[0]['id']
#         return None


#     def get_game_id(self, date_of_match):
#         team_id_1 = self.get_team_id(self.team_1)
#         team_id_2 = self.get_team_id(self.team_2)

#         if not team_id_1:
#             raise ValueError(f"Team ID for {self.team_1} could not be found. Try a different team name variation or match.")
#         if not team_id_2:
#             raise ValueError(f"Team ID for {self.team_2} could not be found. Try a different team name variation or match.")

#         url = f"{self.base_url}/games/h2h?h2h={team_id_1}-{team_id_2}&date={date_of_match}"
#         response = requests.get(url, headers=self.headers)
#         sleep(self.delay)
#         data = response.json().get('response', [{}])
        
#         if not data:
#             raise ValueError("No fixtures found for the given teams and date.")
        
#         return data[0]['id']

#     def get_odds(self,date_of_match):
#         game_id = self.get_game_id(date_of_match)
#         url = f"{self.base_url}/odds?game={game_id}"
#         response = requests.get(url, headers=self.headers)

#         data = response.json().get('response', [{}])
#         if not data:
#             raise ValueError("No odds found for the given teams and date.")
        
#         odds = []
#         bookmakers = data[0]['bookmakers']
#         for i in range(0,3):
#             for bets in bookmakers[i]['bets']:
#                 if bets['name'] == 'Home/Away':
#                     h_b1 = bets['values'][0]['odd']
#                     a_b1 = bets['values'][1]['odd']
#                     odds.append(h_b1)
#                     odds.append(a_b1)

#         odds = list(map(lambda x: float(x), odds))
#         prob = list(map(lambda x: round((1/x)*100,2), odds))
#         return prob

#     def combine_prob(self, date_of_match):
#             probs = self.get_odds(date_of_match)
#             return combine_probabilities((probs[0],probs[1]), (probs[2], probs[3]), (probs[4], probs[5]))


# # def main():
# #     api_key = "69e9ab5f5c6b12f89c5a06cc50b3b106"
# #     team1 = "Washington Nationals"
# #     team2 = "Los Angeles Angels"
# #     date_of_match = "2024-08-11"
# #     bb = BaseBall(api_key, team1, team2)
    
# #     try:
# #         probs = bb.combine_prob(date_of_match)
# #         print(probs)
# #     except ValueError as e:
# #         print(f"Error: {e}")

# # if __name__ == "__main__":
# #     main()
