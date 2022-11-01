from csv import writer
import pandas as pd
import json
import math
import csv
import pprint


# Læser datasættet og erstatter specielle tegn som den ikke var istand til at indkode med orden "aaa"
df = pd.read_csv('data.csv', encoding='UTF-8')
df = df.replace('\ufffd','WZQ', regex=True)
df = df.replace('\u011f','WZQ', regex=True)
df = df.replace('\u0130','WZQ', regex=True)
df = df.replace('\u0148','WZQ', regex=True)
df = df.replace('\u0144','WZQ', regex=True)
df = df.replace('\u0119','WZQ', regex=True)
df = df.replace('\u015f','WZQ', regex=True)
df = df.replace('\u0142','WZQ', regex=True)
df = df.replace('\u015a','WZQ', regex=True)
df = df.replace('\u0105','WZQ', regex=True)
df = df.replace('\u0219','WZQ', regex=True)
df = df.replace('\u021b','WZQ', regex=True)
df = df.replace('\u017a','WZQ', regex=True)
df = df.replace('\u0141','WZQ', regex=True)
df = df.replace('\u00FC','WZQ', regex=True)
df = df.replace('\u00E9','WZQ', regex=True)
df = df.replace('\u00F3','WZQ', regex=True)
df = df.replace('\u00E3','WZQ', regex=True)
df = df.replace('\u00F6','WZQ', regex=True)
df = df.replace('\u00ED','WZQ', regex=True)
df = df.replace('\u00EA','WZQ', regex=True)
df = df.replace('\u00E7','WZQ', regex=True)
df = df.replace('\u00F8','WZQ', regex=True)
df = df.replace('\u00E8','WZQ', regex=True)
df = df.replace('\u00FA','WZQ', regex=True)
df = df.replace('\u00C2','WZQ', regex=True)
df = df.replace('\u00E0','WZQ', regex=True)
df = df.replace('\u00F1','WZQ', regex=True)
df = df.replace('\u00E1','WZQ', regex=True)
df = df.replace('\u00E7','WZQ', regex=True)
df = df.replace('\u00C9','WZQ', regex=True)
df = df.replace('\u00EE','WZQ', regex=True)
df = df.replace('\u00E6','WZQ', regex=True)
df = df.replace('\u00C7','WZQ', regex=True)
df = df.replace('\u00E5','WZQ', regex=True)
df = df.replace('\u00E2','WZQ', regex=True)
df = df.replace('\u00D6','WZQ', regex=True)
df = df.replace('\u00E4','WZQ', regex=True)
df = df.replace('\u00DF','WZQ', regex=True)
df = df.replace('\u00C1','WZQ', regex=True)
df = df.replace('\xa0',' ', regex=True)

def convert(money):
    df[money] = df[money].str.replace("€", "")
    for i, x in enumerate(df[money]):
        column_value = df.at[i, money]
        if "." in column_value and "K" in column_value:
            df.at[i, money] = df.at[i, money].replace(".", "")
            df.at[i, money] = df.at[i, money].replace("K", "00")
            df.at[i, money] = int(df.at[i, money])
        elif "." in column_value and "M" in column_value:
            df.at[i, money] = df.at[i, money].replace(".", "")
            df.at[i, money] = df.at[i, money].replace("M", "00000")
            df.at[i, money] = int(df.at[i, money])
        elif "K" in column_value:
            df.at[i, money] = df.at[i, money].replace("K", "000")
            df.at[i, money] = int(df.at[i, money])
        else:
            df.at[i, money] = df.at[i, money].replace("M", "000000")
            df.at[i, money] = int(df.at[i, money])


convert("Wage")
convert("Value")

drop_list = ["Name", "Special", "PreferredFoot", "InternationalReputation", "WeakFoot", "SkillMoves", "WorkRate", "BodyType", "RealFace", "Position", "JerseyNumber", "Joined", "LoanedFrom",
             "ContractValidUntil", "Height", "Weight", "Age", "Photo", "Nationality", "Flag", "Overall", "Potential", "Club", "ClubLogo", "BestPosition", "BestOverallRating", "ReleaseClause"]
attributes = df.drop(columns=drop_list)
positions = { #changes made here must also be made in the function; splitting_key in position_list
        "GK": [167495, 235073, 190941],
        "RB": [226851, 202371, 253149],
        "LB": [234396, 209889, 239368],
        "CB1": [212190, 229237, 247263],
        "CB2": [220814, 178603, 213331],
        "CDM1": [209658, 218339, 212242],
        "CDM2": [212622, 252371, 211748],
        "COM": [189596, 188350, 213955],
        "HM": [206113, 212194, 202857],
        "LM": [213345, 203486, 241852],
        "ST": [188545, 239085, 234236],
    }
icons = [5003, 7826, 3647, 250, 388, 1183, 48940, 34079, 7512, 53769, 1075, 31432, 45674, 9676, 7289, 13743, 241, 1625, 1198, 138449, 330, 11141, 5680, 121939, 5471, 5589, 1668, 1109, 1088, 5419, 7763, 45661, 23174, 4231, 1040, 28130, 37576, 246, 1256, 13128, 49369, 5984, 51539, 10264, 140601, 10535, 5099, 1041]


def ideal_attributes():
    ideal_player_attributes = {}
    ideal_player_stats = {}

    for position in positions:
        players = positions.get(position)
        for attribute in attributes:
            if attribute == "ID":
                continue
            player_nan_count = 0
            total_attribute_value = 0
            for player in players:
                if math.isnan(df.loc[df["ID"] == player, attribute]):
                    player_nan_count += 1
                    continue
                value = int(df.loc[df["ID"] == player, attribute])
                total_attribute_value += value
            if len(players) == player_nan_count:
                ideal_player_attributes[attribute] = float("nan")
            else:
                attribute_average = round(total_attribute_value/(len(players) - player_nan_count), 1)
            ideal_player_attributes[attribute] = attribute_average
        ideal_player_stats[position] = ideal_player_attributes.copy()
        ideal_player_attributes.clear()
    return ideal_player_stats

#pprint.pprint(ideal_attributes())

def top8(ideal_attributes):
    ideal_attributes = ideal_attributes
    result = {}
    for position in ideal_attributes:
        attributes = ideal_attributes.get(position)
        top8 = sorted(attributes, key=attributes.get, reverse=True)[2:10]
        result[position] = top8
    return result

#pprint.pprint(top8(ideal_attributes()))


def splitting_key():
    team_list = ["FC Bayern MWZQnchen", "Borussia Dortmund", "Leverkusen"]
    position_list = ["GK","RB","LB","CB1","CB2","CDM1","CDM2","COM","HM","LM","ST"]
    # calculate cost of each positions on each team (float)
    ideal_team_cost = {}
    ideal_player_cost = {}
    for x in range(len(team_list)):
        ideal_player_cost.clear()
        for position in positions:
            id = positions.get(position)[x]
            value = float(df.loc[df["ID"] == id, "Wage"] * 52 + df.loc[df["ID"] == id, "Value"])
            ideal_player_cost[position] = value
        ideal_team_cost[team_list[x]] = ideal_player_cost.copy()

    # calculate ratio cost of each position on each team (float)
    ideal_player_ratio_cost_club = {}
    ideal_team_ratio_cost_club = {}
    for club in ideal_team_cost:
        team_cost = 0
        position_costs_array = ideal_team_cost.get(club)
        for position_cost in position_costs_array:
            team_cost += position_costs_array.get(position_cost)
        for position_cost in position_costs_array:
            current_position_cost = position_costs_array.get(position_cost)
            position_ratio_cost = current_position_cost / team_cost
            ideal_player_ratio_cost_club[position_cost] = position_ratio_cost
        ideal_team_ratio_cost_club[club] = ideal_player_ratio_cost_club.copy(
        )

    # calculate average cost in procent of each position from each team (float)
    ideal_team_cost_ratio = {}
    for position in position_list:
        position_ratio = 0
        for club in team_list:
            position_ratio += ideal_team_ratio_cost_club[club].get(position)
    
        average_ratio_position = position_ratio / len(team_list)
        ideal_team_cost_ratio[position] = average_ratio_position
    ideal_team_cost_ratio_sorted = {}
    ratio_to_position = ideal_team_cost_ratio
    ideal_team_cost_ratio_sorted = sorted(ratio_to_position, key=ratio_to_position.get, reverse=True)
    return [ideal_team_cost_ratio, ideal_team_cost_ratio_sorted]

#pprint.pprint(splitting_key())

not_eligible_teams = ["FC Bayern MWZQnchen","Borussia Dortmund","Bayer 04 Leverkusen","RB Leipzig","1. FC Union Berlin","Sport-Club Freiburg","1. FC KWZQln","1. FSV Mainz 05","TSG Hoffenheim","Borussia MWZQnchengladbach","Eintracht Frankfurt","VfL Wolfsburg","VfL Bochum 1848","FC Augsburg","Vfb Stuttgart","Hertha BSC","DSC Arminia Bielefeld"]  # de hold som er i samme liga som holdet.
    
    
eligible_players = []

# Nikolai Kaaberbøl
# Liste med hold:
# 1.	FC Bayern München
# 2.	Borussia Dortmund
# 3.	Bayer 04 Leverkusen
# 4.	RB Leipzig
# 5.	1. FC Union Berlin
# 6.	Sport-Club Freiburg
# 7.	1. FC Köln
# 8.	1. FSV Mainz 05
# 9.	TSG Hoffenheim
# 10.	Borussia Mönchengladbach
# 11.	Eintracht Frankfurt
# 12.	VfL Wolfsburg
# 13.	VfL Bochum 1848
# 14.	FC Augsburg
# 15.	Vfb Stuttgart
# 16.	Hertha BSC
# 17.	DSC Arminia Bielefeld
# 18.	SpVgg Greuther Fürth

def player_list_eligible():
    for player in df["ID"]:
        players_club = df.loc[df["ID"] == player, "Club"].values[0]
        if player in icons:
            continue
        elif players_club in not_eligible_teams:
            continue
        else:
            eligible_players.append(player)
    return eligible_players



def find_best_team(splitting_key, player_id_array, ideal_stats_to_pos, top8_values):
    budget = int(input("budget: "))
    team = {}
    used_player_list = []
    spent = 0
    residual_cash = 0
    splitting_key[1]
    for position in splitting_key[1]:
        player_cost = 0
        new_player = {}
        ideal_stats = ideal_stats_to_pos.get(position)
        for player in player_id_array:
            player_has_Nan = False
            sum_difference = 0
            max_price = budget * splitting_key[0].get(position)
            cost = int(df.loc[df["ID"] == player, "Wage"]) * 52 + int(df.loc[df["ID"] == player, "Value"])
            if cost > max_price + residual_cash or cost == 0:
                continue
            else:
                attribute_count = 0
                for attribute in top8_values[position]:
                    if player_has_Nan:
                        continue
                    if attribute in ["ID", "Value", "Wage"]:
                        continue
                    if math.isnan(df.loc[df["ID"] == player, attribute]):
                        player_has_Nan = True
                        continue
                    else:
                        attribute_count += 1
                        player_attribute_value = float(df.loc[df["ID"] == player, attribute])
                        ideal_attributes_value = ideal_stats.get(attribute)
                        difference = abs(player_attribute_value - ideal_attributes_value) * 1  # WEIGHTED NUMBER
                    sum_difference += difference
            if player_has_Nan == False:
                sum_difference_average = sum_difference / attribute_count
                if player not in used_player_list:
                    new_potential_player = {}
                    if new_player.get(position) == None:
                        new_player[position] = [player, str(df.loc[df["ID"] == player, "Name"].values[0]), sum_difference_average, cost]
                        player_cost = cost
                    else:
                        new_potential_player[position] = [player, str(df.loc[df["ID"] == player, "Name"].values[0]), sum_difference_average, cost]
                        player_stat_values = new_potential_player[position][2]
                        if player_stat_values < new_player[position][2]:
                            new_player[position] = [player, str(df.loc[df["ID"] == player, "Name"].values[0]), sum_difference_average, cost]
                            player_cost = cost
            else: 
                continue  
        residual_cash = max_price + residual_cash - player_cost
        used_player_list.append(new_player[position][0])
        spent += new_player[position][3]                
        team[position] = new_player[position].copy()
        print(new_player, residual_cash)
    procent_spent = spent*100 / budget
    return team, spent, procent_spent


pprint.pprint(find_best_team(splitting_key = splitting_key(), player_id_array= player_list_eligible(), ideal_stats_to_pos= ideal_attributes(), top8_values = top8(ideal_attributes())))

