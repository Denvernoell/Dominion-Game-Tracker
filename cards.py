import streamlit as st
import pandas as pd

# Get cards
tables = pd.read_html(
    "http://wiki.dominionstrategy.com/index.php/List_of_cards")
df = tables[0]
sets = [s for s in df['Set'].unique()]

players = ['Jerod', 'Sawyer', 'Denver', 'Courtney', 'Noah']

st.header("Dominion Game Adder")
st.text("Add game below")

# my_set = st.selectbox("Select sets", sets)
# my_cards = [c for c in df[df['Set'] == my_set]['Name']]
my_cards = [c for c in df['Name']]


game_cards = st.multiselect("Select card", my_cards)
my_players = st.multiselect("Players", players)

# class Player:
# 	def __init__(self,name,score):
# 		self.name = name
# 		self.score = score
# Player(player,score)

player_scores = {}

for player in my_players:
    player_scores[player] = st.number_input(f"{player} Score", step=1)

if len(my_players) > 1:

    player_tiebreakers = {}
    score_check = sorted(player_scores.items(),
                         key=lambda x: x[1], reverse=True)
    if score_check[0][1] == score_check[1][1] and score_check[0][1] != 0:
        for player in my_players:
            player_tiebreakers[player] = st.checkbox(f"{player} Tiebreaker")

# st.write(player_scores)


if st.button("Submit game"):
    with open('game_data.txt', 'w') as f:
        for card in game_cards:
            f.write(card)
            f.write('\n')
