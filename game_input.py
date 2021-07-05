import streamlit as st
import pandas as pd
from datetime import datetime


players = ['Jerod', 'Sawyer', 'Denver', 'Courtney', 'Noah']

st.header("Dominion Game Adder")
st.text("Add game below")


# Get cards
tables = pd.read_html(
    "http://wiki.dominionstrategy.com/index.php/List_of_cards")
df = tables[0]


exclusions = ['Knight', 'Ruins', 'Prize', 'Shelter', 'Traveller',
              'Castle', 'Spirit', 'Zombie', 'Boon', 'Hex', 'State', 'Artifact']
additions = ['Knights', 'Ruins', 'Shelters', 'Page', 'Peasant', 'Castles']
exclusion_ids = [i for i, t in zip(df.index, df['Types'])
                 for e in exclusions if t.find(e) != -1]


my_cards = [c for c in df.drop(exclusion_ids)['Name']]
my_cards += additions


game_cards = st.multiselect("Select card", my_cards)
my_players = st.multiselect("Players", players)


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


if st.button("Submit game"):
    games = pd.read_excel('Dominion_games.xlsx', sheet_name='Games')

    row = {

        'Date': datetime.now().date(),
        'Cards': game_cards,
        'Scores': player_scores,
    }
    games = games.append(row, ignore_index=True)
    games.to_excel("Dominion_games.xlsx", sheet_name='Games', index=False)

    st.success('Added Game')
