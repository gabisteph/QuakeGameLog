from jinja2 import Environment, FileSystemLoader
import json
import pandas as pd
import matplotlib.pyplot as plt
import pdfkit




def generate_summary_report():
    """
    Generates a summary report for a Quake game log.

    This function reads a JSON file containing game data, processes the data, and generates a summary report in HTML format.
    The report includes three tables: 
    - Table 1: Game statistics including the total number of kills, number of players, best player, and player with the most deaths for each game.
    - Table 2: Top 5 players with the highest number of matches played.
    - Table 3: Top 5 players with the highest number of kills across all matches.

    The function also generates a bar chart showing the number of kills for the top 5 players.

    The generated HTML report and bar chart image are saved to files.

    Returns:
    None
    """
    # read gamedata JSON
    with open('gamedata.json', 'r') as f:
        games = json.load(f)
    with open('deathMatches.json', 'r') as f:
        deaths = json.load(f)
    # Format the data for the DataFrame gamedata
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
    # Format the data for the DataFrame deathdata
    deaths_temp = []
    for death in deaths:
        valuegame, details = list(death.items())[0]
        death = {
            "Game": valuegame,
            "kills_by_means": details.get("deaths", {})
        }
        deaths_temp.append(death)

    # Create a DataFrame gamedata
    df = pd.DataFrame(records)
    # Matrix of the DataFrame
    matriz = df.values
    # Create a DataFrame deathdata
    df4 = pd.DataFrame(deaths)
    # Matrix of the DataFrame
    matriz2 = df4.values
    # Construct table 1
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
    
    # Create table 1
    df_tab1 = pd.DataFrame(dict_tab1).set_index("Game").reset_index()
    # Create table deaths
    df_tabDeaths = pd.DataFrame(df4)
    # filter players and number of matchs
    dict_players = {}
    for line in matriz:
        match_players = line[1]
        for player in match_players:
            if player not in dict_players:
                dict_players[player] = 1
            else:
                dict_players[player] +=1

    # Construct table 2
    dict_tab2 = {
        "Players": list(dict_players.keys()),
        "Number of Matchs": list(dict_players.values())
    }
    df_tab2 = pd.DataFrame(dict_tab2).sort_values(by=["Number of Matchs"],ascending=False).head(5)

    # filtrar players e número de kills
    dict_players = {}
    for line in matriz:
        match_players = line[1]
        kills_players = line[3]
        for player in match_players:
            if player in kills_players:
                if player in dict_players:
                    dict_players[player] += kills_players[player]
                else:
                    dict_players[player] = kills_players[player]

    # Construct table 3
    dict_tab3 = {
        "Players": list(dict_players.keys()),
        "Number of Kills all Matchs": list(dict_players.values())
    }
    df_tab3 = pd.DataFrame(dict_tab3).sort_values(by=["Number of Kills all Matchs"],ascending=True).head(5)

    # Load the template environment
    env = Environment(loader=FileSystemLoader('.'))

    # Load the template
    template = env.get_template('templates/template.html')

    # Define the data tab 1 for the template
    columns_tab1 = df_tab1.columns.tolist()
    data_tab1 = df_tab1.to_dict(orient='records')

    # Define the data tab 2 for the template
    columns_tab2 = df_tab2.columns.tolist()
    data_tab2 = df_tab2.to_dict(orient='records')

    # Define the data tab 2 for the template
    columns_tab3 = df_tab3.columns.tolist()
    data_tab3 = df_tab3.to_dict(orient='records')
    
    # Define the data tab deaths for the template
    columns_tab4 = df_tabDeaths.columns.tolist()
    data_tab4 = df_tabDeaths.to_dict(orient='records')

    # Render the template with the data
    html_output = template.render(columns_tab1=columns_tab1, data_tab1=data_tab1, 
                                  columns_tab2=columns_tab2, data_tab2=data_tab2,
                                  columns_tab3=columns_tab3, data_tab3=data_tab3,
                                  columns_tab4=columns_tab4, data_tab4=data_tab4)

    # Save the rendered HTML to a file
    with open('templates/report.html', 'w') as f:
        f.write(html_output)

    # genarate bar chart
    df_tab3.plot(kind='bar', x='Players', y='Number of Kills all Matchs', color='#3f70c5')

    # Adicionando título e rótulos aos eixos
    plt.title('Top 5 Best Players')
    plt.xlabel('Players')
    plt.ylabel('Number of Kills')
    plt.xticks(rotation=0)  # Rotacionar os rótulos em 90 graus

    # Salvar o gráfico em um arquivo
    plt.savefig('assets/bar_chart.png')

    

    print("Report HTML generated successfully.")

if __name__ == "__main__":
    generate_summary_report()