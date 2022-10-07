import pandas as pd
import json

#Læser datasættet og erstatter specielle tegn som den ikke var istand til at indkode med orden "aaa"
df = pd.read_csv('data.csv', encoding='UTF-8')
df=df.replace('\ufffd','aaa',regex=True)

def ideal_attributes():
    positions = {
        "CM": [212198, 209658, 176580, 192985],
        "CAM": [240558, 262846, 241317, 259646]
    }
    attributes = ["Strength","Agility","Aggression"]

    ideal_player_attributes = {}
    ideal_player_stats = {}

    for position in positions:
        players = positions.get(position)
        for attribute in attributes:
            total_attribute_value = 0
            for player in players:
                value = int(df.loc[df["ID"] == player, attribute])
                total_attribute_value += value
            attribute_average = total_attribute_value/len(players)
            ideal_player_attributes[attribute] = attribute_average
        ideal_player_stats[position] = ideal_player_attributes.copy()
        ideal_player_attributes.clear()
    print(ideal_player_stats)

#ideal_attributes()




for x in df.Value:
    x = x.replace("€", "")
    if "." in x and "K" in x:
        x = x.replace(".", "")
        x = x.replace("K", "00")
    elif "." in x and "M" in x:
        x = x.replace(".", "")
        x = x.replace("M", "00000")
    elif "K" in x:
        x = x.replace("K", "000")
    else:
        x = x.replace("M", "000000")
    print(int(x))




































formation = {
    "4-2-3": {
        "CM": {
            "name": "Benny",
            "age": 28,
            "atk": 80,
            "def": 23,
        },
        "CAM": {
            "name": "Bob",
            "age": 32,
            "atk": 70,
            "def": 56,
        },
    },
    "4-2-1": {
       "GK": {
            "name": "John",
            "age": 48,
            "atk": 83,
            "def": 43,
        },
        "ST": {
            "name": "James",
            "age": 31,
            "atk": 72,
            "def": 54,
        }, 
    }
}






