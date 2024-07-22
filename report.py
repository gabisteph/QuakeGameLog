from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import json
import pandas as pd


# Carregar o JSON
with open('gamedata.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

# Transformar a lista de jogos em um formato de DataFrame
records = []
for game in games:
    game_name, details = list(game.items())[0]
    record = {
        "Game": game_name,
        "Players": details.get("players", []),
        "Total Kills": details.get("total_kills", None),
        "Kills": details.get("kills", {})
    }
    records.append(record)

# Criar o DataFrame
df = pd.DataFrame(records)
# Matriz da df
matriz = df.values

# Construir tabela 1
dict_tab1 = {
    "Game": [],
    "Total Kills": [],
    "Numbers of Players":[],
    "Best Player":[],
    "Player Witch Most Deaths":[]
}
for line in matriz:
    dict_tab1["Game"].append(line[0])
    dict_tab1["Numbers of Players"].append(int(len(line[1])))
    if pd.notna(line[2]):
        dict_tab1["Total Kills"].append(int(line[2]))
    else:
        dict_tab1["Total Kills"].append(0)
    if line[3]!={}:
        min_key = min(line[3], key=line[3].get)
        dict_tab1["Best Player"].append(min_key)
        max_key = max(line[3], key=line[3].get)
        dict_tab1["Player Witch Most Deaths"].append(max_key)
    else:
        dict_tab1["Best Player"].append(0)
        dict_tab1["Player Witch Most Deaths"].append(0)

#print(dict_tab1)
# Criar dataframe da tabela 1
df_tab1 = pd.DataFrame(dict_tab1).set_index("Game").reset_index()
#print(df_tab1)

# filtrar players e número de partidas
dict_players = {}
for line in matriz:
    match_players = line[1]
    for player in match_players:
        if player not in dict_players:
            dict_players[player] = 1
        else:
            dict_players[player] +=1
# Contruir a tabela 2
dict_tab2 = {
    "Players": list(dict_players.keys()),
    "Number of Matchs": list(dict_players.values())
}
df_tab2 = pd.DataFrame(dict_tab2).sort_values(by=["Number of Matchs"],ascending=False).head(5)
print(df_tab2)   



# Load the template environment
env = Environment(loader=FileSystemLoader('.'))

# Load the template
template = env.get_template('template.html')

# Define the data tab 1 for the template
columns_tab1 = df_tab1.columns.tolist()
data_tab1 = df_tab1.to_dict(orient='records')
# Define the data tab 2 for the template
columns_tab2 = df_tab2.columns.tolist()
data_tab2 = df_tab2.to_dict(orient='records')

# Render the template with the data
html_output = template.render(columns_tab1=columns_tab1, data_tab1=data_tab1, columns_tab2=columns_tab2, data_tab2=data_tab2)

# Save the rendered HTML to a file
with open('summary.html', 'w') as f:
    f.write(html_output)

print("Summary HTML generated successfully.")
