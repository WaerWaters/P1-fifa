import pandas as pd
import json

#Læser datasættet og erstatter specielle tegn som den ikke var istand til at indkode med orden "aaa"
df = pd.read_csv('data.csv', encoding='UTF-8')
df=df.replace('\ufffd','aaa',regex=True)

def convert(money):
    df[money] = df[money].str.replace("€", "")
    for i,x in enumerate(df[money]):
        column_value = df.at[i,money] 
        if "." in column_value and "K" in column_value:
            df.at[i,money] = df.at[i,money].replace(".", "")
            df.at[i,money] = df.at[i,money].replace("K", "00")
            df.at[i,money] = int(df.at[i,money])
        elif "." in column_value and "M" in column_value:
            df.at[i,money] = df.at[i,money].replace(".", "")
            df.at[i,money] = df.at[i,money].replace("M", "00000")
            df.at[i,money] = int(df.at[i,money])
        elif "K" in column_value:
            df.at[i,money] = df.at[i,money].replace("K", "000")
            df.at[i,money] = int(df.at[i,money])
        else:
            df.at[i,money] = df.at[i,money].replace("M", "000000")
            df.at[i,money] = int(df.at[i,money])

convert("Wage")
convert("Value")

drop_list = ["Name"]
attributes = df.drop(columns=drop_list)
positions = {
        "GK": [167495, 235073, 190941],
        "RB": [226851, 202371, 253149],
        "LB": [234396, 209889, 239368],
        "CB": [212190, 229237, 247263, 220814, 178603, 213331],
        "CDM": [209658, 218339, 212242, 212622, 252371, 211748],
        "COM": [189596, 188350, 213955],
        "HM": [206113, 212194, 202857],
        "LM": [213345, 203486, 241852],
        "ST": [188545, 239085, 234236],
    }

def ideal_attributes():
    

    ideal_player_attributes = {}
    ideal_player_stats = {}

    for position in positions:
        players = positions.get(position)
        for attribute in attributes:
            total_attribute_value = 0
            for player in players:
                value = int(df.loc[df["ID"] == player, attribute])
                total_attribute_value += value
            attribute_average = round(total_attribute_value/len(players),1)
            ideal_player_attributes[attribute] = attribute_average
        ideal_player_stats[position] = ideal_player_attributes.copy()
        ideal_player_attributes.clear()
    ideal_player_stats_json = json.dumps(ideal_player_stats, indent=2)
    print(ideal_player_stats_json)
    return ideal_player_stats, positions

def splitting_key():
    team_list = ["Bayern Munchen", "Dortmund", "Leverkusen"]
    ideal_team_cost = {}
    ideal_player_cost = {}
    for x in range(len(team_list)):
        ideal_player_cost.clear()
        for position in positions:
            if position == "CB" or position == "CDM":
                first = positions.get(position)[x]
                second = positions.get(position)[x+3]
                first = float(df.loc[df["ID"] == first, "Wage"] * 52 + df.loc[df["ID"] == first, "Value"])
                second = float(df.loc[df["ID"] == second, "Wage"] * 52 + df.loc[df["ID"] == second, "Value"])
                value = (first + second)/2
                ideal_player_cost[position] = value
            else:
                id = positions.get(position)[x]
                value = float(df.loc[df["ID"] == id, "Wage"] * 52 + df.loc[df["ID"] == id, "Value"])
                ideal_player_cost[position] = value
        ideal_team_cost[team_list[x]] = ideal_player_cost.copy()
    ideal_team_cost_json = json.dumps(ideal_team_cost, indent=2)
    print(ideal_team_cost_json)
    return ideal_player_cost
    
splitting_key()

def find_best_team(splitting_key, player_id_array, ideal_stats_to_pos, position_id):
    budget = 0
    team = {}
    for position in ideal_stats_to_pos:
        new_player = {}
        ideal_stats = ideal_stats_to_pos.get(position)
        sum_difference = 0
        for player in player_id_array:
            max_price = budget * splitting_key
            cost = int(df.loc[df["ID"] == player, "Wage"]) * 52 + int(df.loc[df["ID"] == player, "Value"])
            if cost > max_price:
                continue
            else:
                attribute_count = 0
                for attribute in attributes.columns:
                    attribute_count += 1
                    player_attribute_value = df.loc[df["ID"] == player, attribute]
                    ideal_attributes_value = ideal_stats.get(attributes)
                    weighted_difference= abs(player_attribute_value - ideal_attributes_value) * 1 #WEIGHTED NUMBER
                    sum_difference += weighted_difference
            sum_difference_average = sum_difference / attribute_count
            if new_player.get(position) == None:
                new_player[position] = [player, sum_difference_average]
            else:
                player_stat_values = new_player[position]
                if sum_difference_average < player_stat_values[1]:
                    new_player[position] = [player, sum_difference_average]
        team[position] = new_player[position]

            

#splitting key
#drop list
#convert "Wage" and "Value" to int

            
            


    

#ideal_attributes()
#find_best_team(1, df["ID"], ideal_attributes())








































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






