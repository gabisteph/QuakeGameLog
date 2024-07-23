import re
import json

def readLog():
    """
    Reads the log file and returns a list of lines.

    Returns:
    lines (list): A list of lines from the log file.
    """
    infile = r"logs\qgames.log"
    with open(infile, 'r') as file:
        lines = file.readlines()
    return lines

def currentGame(lines):
    """
    Parses the log lines and extracts information about each game.

    Args:
    lines (list): A list of lines from the log file.

    Returns:
    gameMatchs (list): A list of dictionaries containing information about each game.
    """
    gameMatchs = []
    deathMatchs = []
    allDeaths = {}
    meansDeaths = {}
    currentGame = {}
    game = 0
    for line in lines:
        if re.search(r'InitGame', line):
            game += 1
            currentGame = {"Game " + str(game): {}}
            meansDeaths = {"Game " + str(game): {}}
            gameMatchs.append(currentGame)
            deathMatchs.append(meansDeaths)
        if re.search(r'ClientUserinfoChanged', line):
            piece = line.split('n\\')
            if len(piece) > 1:
                name = piece[1].split('\\')[0]
            if "players" not in currentGame["Game " + str(game)]:
                currentGame["Game " + str(game)]["players"] = []
                currentGame["Game " + str(game)]["players"].append(name)
            else:
                currentGame["Game " + str(game)]["players"].append(name)

        if re.search(r'Kill:', line):
            if "total_kills" not in currentGame["Game " + str(game)]:
                currentGame["Game " + str(game)]["total_kills"] = 1
            else:
                currentGame["Game " + str(game)]["total_kills"] += 1
            piece = line.split('killed ')
            if len(piece) > 1:
                namekill = piece[1].split(' by')[0]

            if "kills" not in currentGame["Game " + str(game)]:
                currentGame["Game " + str(game)]["kills"] = {}
                if not re.search(r'<world>', line):
                    currentGame["Game " + str(game)]["kills"][namekill] = 1
                else:
                    currentGame["Game " + str(game)]["kills"][namekill] = -1
            else:
                if namekill not in currentGame["Game " + str(game)]["kills"]:
                    if not re.search(r'<world>', line):
                        currentGame["Game " + str(game)]["kills"][namekill] = 1
                    else:
                        currentGame["Game " + str(game)]["kills"][namekill] = -1
                else:
                    if not re.search(r'<world>', line):
                        currentGame["Game " + str(game)]["kills"][namekill] += 1
                    else:
                        currentGame["Game " + str(game)]["kills"][namekill] -= 1
                cause = line.split('by ')
                if len(cause) > 1:
                    kindDeath = cause[1].split(' by')[0]
                if "kills_by_means" not in meansDeaths["Game " + str(game)]:
                    meansDeaths["Game " + str(game)]["kills_by_means"] = {}
                    meansDeaths["Game " + str(game)]["kills_by_means"][kindDeath] = 1
                else:
                    if kindDeath not in meansDeaths["Game " + str(game)]["kills_by_means"]:
                        meansDeaths["Game " + str(game)]["kills_by_means"][kindDeath] = 1
                    else:
                        meansDeaths["Game " + str(game)]["kills_by_means"][kindDeath] += 1
            
    
    return gameMatchs, deathMatchs




def main():
    """
    Reads the log file, processes the game data, and saves it to a JSON file.
    """
    lines = readLog()
    gameMatchs, meansDeaths = currentGame(lines)

    with open("gamedata.json", "w") as outfile:
        json.dump(gameMatchs, outfile, indent=1)
    with open("deathMatches.json", "w") as outfile:
        json.dump(meansDeaths, outfile, indent=1)

if __name__ == "__main__":
    main()


            
