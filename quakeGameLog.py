import re
import json

def readLog():
    infile = r"logs\qgames.log"
    with open(infile, 'r') as file:
        lines = file.readlines()
    return lines

def currentGame(lines):
    gameMatchs = []
    currentGame = {};
    game = 0
    for line in lines:
        if re.search(r'InitGame', line):
            game +=1
            currentGame = { "Game "+ str(game): {}}
            gameMatchs.append(currentGame)
        if re.search(r'ClientUserinfoChanged', line):
            piece = line.split('n\\')
            if len(piece) > 1:
                name = piece[1].split('\\')[0]
            if "players" not in currentGame["Game "+ str(game)]:
                currentGame["Game "+ str(game)]["players"] = []
                currentGame["Game "+ str(game)]["players"].append(name)
            else:
                currentGame["Game "+ str(game)]["players"].append(name)
            

        if re.search(r'Kill:',line):
            if "total_kills" not in currentGame["Game "+ str(game)]:
                currentGame["Game "+ str(game)]["total_kills"] = 1
            else:
                currentGame["Game "+ str(game)]["total_kills"] +1
            piece = line.split('killed ')
            if len(piece)>1:
                namekill = piece[1].split(' by')[0]
            
            if "kills" not in currentGame["Game "+ str(game)]:
                currentGame["Game "+ str(game)]["kills"] = {}
                if not re.search(r'<world>',line):
                    currentGame["Game "+ str(game)]["kills"][namekill] = 1
                else:
                    currentGame["Game "+ str(game)]["kills"][namekill] = -1
            else:
                if namekill not in currentGame["Game "+ str(game)]["kills"]:
                    if not re.search(r'<world>',line):
                        currentGame["Game "+ str(game)]["kills"][namekill] = 1
                    else:
                        currentGame["Game "+ str(game)]["kills"][namekill] = -1
                else:
                    if not re.search(r'<world>',line):
                        currentGame["Game "+ str(game)]["kills"][namekill] +=1
                    else:
                        currentGame["Game "+ str(game)]["kills"][namekill] -=1
            
        
       
    return gameMatchs


def main():
    lines = readLog()
    games = currentGame(lines)
    json_object = json.dumps(games)
    with open("gamedata.json", "w") as outfile:
        outfile.write(json_object)


if __name__ == "__main__":
    main()


            
