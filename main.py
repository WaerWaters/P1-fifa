from csv import writer
import pandas as pd
import json
import math
import csv
import pprint
import numpy as np
import matplotlib.pyplot as plt



# Læser datasættet og erstatter specielle tegn som den ikke var istand til at indkode med orden "aaa"
df = pd.read_csv('data.csv', encoding='UTF-8')
pd.set_option('display.max_rows', None)
pd.options.display.float_format = '{:.2f}'.format
df.head()

uni_array = ['\ufffd','\u015f','\u011f','\u0130','\u0148','\u0119','\u0142','\u015a','\u0105','\u0219','\u021b','\u017a','\u0141','\u00FC','\u00E9','\u00F3','\u00E3','\u00F6','\u00ED','\u00EA','\u00E7','\u00F8','\u00E8','\u00FA','\u00C2','\u00E0','\u00F1','\u00E1','\u00C9','\u00EE','\u00E6','\u00C7','\u00E5','\u00E2','\u00D6','\u00E4','\u00DF','\u00C1']
for uni in uni_array:
    df = df.replace(uni,'WZQ', regex=True)
df = df.replace('\xa0',' ', regex=True)

df["Wage"] = df["Wage"].replace({"K": "*1e3" ,"€": "", "M": "*1e6"}, regex=True).map(pd.eval).astype(float).round(4)
df["Value"] = df["Value"].replace({"K": "*1e3" ,"€": "", "M": "*1e6"}, regex=True).map(pd.eval).astype(float).round(4)

drop_list = ["Name", "Special", "PreferredFoot", "InternationalReputation", "WeakFoot", "SkillMoves", "WorkRate", "BodyType", "RealFace", "Position", "JerseyNumber", "Joined", "LoanedFrom","ContractValidUntil", "Height", "Weight", "Age", "Photo", "Nationality", "Flag", "Overall", "Potential", "Club", "ClubLogo", "BestPosition", "BestOverallRating", "ReleaseClause"]
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



def ideal_attributes():
    ideal_position_attribute = {}
    ideal_team_attributes = {}

    for position in positions:
        ideal_position_attribute.clear()
        players = positions.get(position)
        for attribute in attributes:
            if attribute == "ID":
                continue
            players_with_NaN = 0
            total_attribute_value = 0
            for player in players:
                if math.isnan(df.loc[df["ID"] == player, attribute]):
                    players_with_NaN += 1
                    continue
                attribute_value = int(df.loc[df["ID"] == player, attribute])
                total_attribute_value += attribute_value
            if len(players) == players_with_NaN:
                ideal_position_attribute[attribute] = float("nan")
            else:
                attribute_average = round(total_attribute_value/(len(players) - players_with_NaN), 1)
            ideal_position_attribute[attribute] = attribute_average
        ideal_team_attributes[position] = ideal_position_attribute.copy()
    return ideal_team_attributes

#pprint.pprint(ideal_attributes())

def top8(ideal_team_attributes):
    result = {}
    for position in ideal_team_attributes:
        attributes = ideal_team_attributes.get(position)
        top8 = sorted(attributes, key=attributes.get, reverse=True)[2:10]
        result[position] = top8
    return result

#pprint.pprint(top8(ideal_attributes()))


def splitting_key():
    top_clubs = ["FC Bayern MWZQnchen", "Borussia Dortmund", "Leverkusen"]
    # calculate cost of each positions on each team (float)
    top_clubs_costs = {}
    ideal_player_cost = {}
    for team_id, team in enumerate(top_clubs):
        ideal_player_cost.clear()
        for position in positions:
            id = positions.get(position)[team_id]
            total_player_cost = float(df.loc[df["ID"] == id, "Wage"] * 52 + df.loc[df["ID"] == id, "Value"])
            ideal_player_cost[position] = total_player_cost
        top_clubs_costs[team] = ideal_player_cost.copy()

    # calculate ratio cost of each position on each team (float)
    club_position_ratio = {}
    top_clubs_ratios = {}
    for club in top_clubs_costs:
        team_total_cost = 0
        positions_costs = top_clubs_costs.get(club)
        team_total_cost = sum(positions_costs.values())
        for position_cost in positions_costs:
            position_cost_ratio = positions_costs.get(position_cost) / team_total_cost
            club_position_ratio[position_cost] = position_cost_ratio
        top_clubs_ratios[club] = club_position_ratio.copy()

    # calculate average cost ratio of each position from each club (float)
    ideal_club_cost_ratio = {}
    ideal_club_ratio_sorted = {}
    for position in positions:
        sum_position_ratio = 0
        for club in top_clubs:
            sum_position_ratio += top_clubs_ratios[club].get(position)
        position_average_ratio = sum_position_ratio / len(top_clubs)
        ideal_club_cost_ratio[position] = position_average_ratio
    ideal_club_ratio_sorted = sorted(ideal_club_cost_ratio, key=ideal_club_cost_ratio.get, reverse=True)
    return [ideal_club_cost_ratio, ideal_club_ratio_sorted]

#pprint.pprint(splitting_key())


not_eligible_teams = ["FC Bayern MWZQnchen","Borussia Dortmund","Bayer 04 Leverkusen","RB Leipzig","1. FC Union Berlin","Sport-Club Freiburg","1. FC KWZQln","1. FSV Mainz 05","TSG Hoffenheim","Borussia MWZQnchengladbach","Eintracht Frankfurt","VfL Wolfsburg","VfL Bochum 1848","FC Augsburg","Vfb Stuttgart","Hertha BSC","DSC Arminia Bielefeld"]  # de hold som er i samme liga som holdet.
eligible_players = []
icon_ids = [5003, 7826, 3647, 250, 388, 1183, 48940, 34079, 7512, 53769, 1075, 31432, 45674, 9676, 7289, 13743, 241, 1625, 1198, 138449, 330, 11141, 5680, 121939, 5471, 5589, 1668, 1109, 1088, 5419, 7763, 45661, 23174, 4231, 1040, 28130, 37576, 246, 1256, 13128, 49369, 5984, 51539, 10264, 140601, 10535, 5099, 1041]

def eligible_players_list():
    for player in df["ID"]:
        players_club = df.loc[df["ID"] == player, "Club"].values[0]
        if player in icon_ids:
            continue
        elif players_club in not_eligible_teams:
            continue
        else:
            eligible_players.append(player)
    return eligible_players

#pprint.pprint(eligible_players_list())


def find_best_team(splitting_key, players, ideal_stats_to_pos, top8_values):
    budget = int(input("budget: "))
    team = {}
    used_player_list = []
    spent = 0
    residual_cash = 0
    for position in splitting_key[1]:
        player_chosen = []
        ideal_stats = ideal_stats_to_pos.get(position)
        for player in players:
            player_has_NaN = False
            sum_difference = 0
            max_price = budget * splitting_key[0].get(position)
            player_cost = int(df.loc[df["ID"] == player, "Wage"]) * 52 + int(df.loc[df["ID"] == player, "Value"])
            if player_cost > max_price + residual_cash or player_cost == 0:
                continue
            else:
                attribute_count = 0
                for attribute in top8_values[position]:
                    if player_has_NaN:
                        continue
                    if attribute in ["ID", "Value", "Wage"]:
                        continue
                    if math.isnan(df.loc[df["ID"] == player, attribute]):
                        player_has_NaN = True
                        continue
                    else:
                        attribute_count += 1
                        player_attribute_value = float(df.loc[df["ID"] == player, attribute])
                        ideal_attribute_value = ideal_stats.get(attribute)
                        difference = abs(player_attribute_value - ideal_attribute_value) * 1  # WEIGHTED NUMBER
                        sum_difference += difference
            if player_has_NaN == False:
                if player not in used_player_list:
                    sum_difference_average = sum_difference / attribute_count
                    potential_player = [player, str(df.loc[df["ID"] == player, "Name"].values[0]), sum_difference_average, player_cost]
                    if player_chosen == []:
                        player_chosen = potential_player
                    else:
                        if potential_player[2] < player_chosen[2]:
                            player_chosen = potential_player
            else:
                continue  
        residual_cash = max_price + residual_cash - player_chosen[3]
        used_player_list.append(player_chosen[0])
        spent += player_chosen[3]                
        team[position] = player_chosen
        print(player_chosen, residual_cash)
    procent_spent = spent*100 / budget
    return team, spent, procent_spent


pprint.pprint(find_best_team(splitting_key = splitting_key(), players= eligible_players_list(), ideal_stats_to_pos= ideal_attributes(), top8_values = top8(ideal_attributes())))
