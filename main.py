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


df["Wage"] = df["Wage"].replace({"K": "*1e3" ,"€": "", "M": "*1e6"}, regex=True).map(pd.eval).astype(float).round(4)
df["Value"] = df["Value"].replace({"K": "*1e3" ,"€": "", "M": "*1e6"}, regex=True).map(pd.eval).astype(float).round(4)

drop_list = ["Name", "Special", "PreferredFoot", "InternationalReputation", "WeakFoot", "SkillMoves", "WorkRate", "BodyType", "RealFace", "Position", "JerseyNumber", "Joined", "LoanedFrom","ContractValidUntil", "Height", "Weight", "Age", "Photo", "Nationality", "Flag", "Overall", "Potential", "Club", "ClubLogo", "BestPosition", "BestOverallRating", "ReleaseClause", "Marking"]
attributes = df.drop(columns=drop_list)
positions = {
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
                total_attribute_value += int(df.loc[df["ID"] == player, attribute])
            if len(players) == players_with_NaN:
                ideal_position_attribute[attribute] = float("nan")
            else:
                attribute_average = round(total_attribute_value/(len(players) - players_with_NaN), 1)
            ideal_position_attribute[attribute] = attribute_average
        ideal_team_attributes[position] = ideal_position_attribute.copy()
    return ideal_team_attributes

#pprint.pprint(ideal_attributes())

def top11(ideal_team_attributes):
    result = {}
    for position in ideal_team_attributes:
        attributes = ideal_team_attributes.get(position)
        top11 = sorted(attributes, key=attributes.get, reverse=True)[2:13]
        result[position] = top11
    return result

#pprint.pprint(top11(ideal_attributes()))


def splitting_key():
    top_clubs = ["FC Bayern München", "Borussia Dortmund", "Leverkusen"]
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




def eligible_players_list():
    not_eligible_teams = ["FC Bayern München","Borussia Dortmund","Bayer 04 Leverkusen","RB Leipzig","1. FC Union Berlin","Sport-Club Freiburg","1. FC Köln","1. FSV Mainz 05","TSG Hoffenheim","Borussia Mönchengladbach","Eintracht Frankfurt","VfL Wolfsburg","VfL Bochum 1848","FC Augsburg","Vfb Stuttgart","Hertha BSC","DSC Arminia Bielefeld","Deportivo Táchira FC","Club Olimpia","Club Nacional de Football","Junior FC","Club Cerro Porteño","Barcelona Sporting Club","Universidad Católica","Club Universitario de Deportes", "Club Always Ready","América de Cali","LDU Quito", "Club Sporting Cristal", "Club Atlético Rentistas","Atlético Nacional","Flamengo","Palmeiras","São Paulo","Club Independiente Santa Fe", "Club The Strongest","Independiente del Valle", "Unión La Calera","Deportivo La Guaira FC","Sport Club Corinthians Paulista","Deportivo Cali","RB Bragantino","Club Atlético Peñarol","CD Huachipato","Club Bolívar","Club Libertad","Club Deportes Tolima","Montevideo City Torque","Carlos A. Mannucci","Universidad Técnica de Cajamarca","Deportivo Pasto","CS Emelec","Club Deportivo Palestino","Guaireña FC","Club River Plate Asunción","Sport Huancayo","Club Deportivo Jorge Wilstermann","La Equidad","CD Antofagasta","12 de Octubre FC","Guayaquil City FC","Centro Atlético Fénix","Cerro Largo Fútbol Club","Club de Deportes Cobresal","Club Social y Deportivo Macará","Academia Puerto Cabello","FBC Melgar","Metropolitanos de Caracas FC","Club Atlético Nacional Potosí","Aragua Fútbol Club","Club Deportivo Guabirá","AC Mineros de Guayana"]  # de hold som er i samme liga som holdet og de hold som ikke er i Fifa
    icon_ids = [5003, 7826, 3647, 250, 388, 1183, 48940, 34079, 7512, 53769, 1075, 31432, 45674, 9676, 7289, 13743, 241, 1625, 1198, 138449, 330, 11141, 5680, 121939, 5471, 5589, 1668, 1109, 1088, 5419, 7763, 45661, 23174, 4231, 1040, 28130, 37576, 246, 1256, 13128, 49369, 5984, 51539, 10264, 140601, 10535, 5099, 1041]
    not_found_ingame = [230289, 173155]
    eligible_players = []
    for player in df["ID"]:
        players_club = df.loc[df["ID"] == player, "Club"].values[0]
        player_name = df.loc[df["ID"] == player, "Name"].values[0]
        if (player in icon_ids) or (player in not_found_ingame) or (players_club in not_eligible_teams) or (any(char.isdigit() for char in player_name)):
            continue
        else:
            eligible_players.append(player)
    return eligible_players

#pprint.pprint(eligible_players_list())


def find_best_team(splitting_key, players, ideal_stats_to_pos, top11_values):
    budget = int(input("budget: "))
    team = {}
    used_player_list = []
    spent = 0
    residual_cash = 0
    for position in splitting_key[1]:
        player_chosen = []
        ideal_stats = ideal_stats_to_pos.get(position)
        max_price = budget * splitting_key[0].get(position)
        for player in players:
            player_has_NaN = False
            sum_difference = 0
            player_cost = int(df.loc[df["ID"] == player, "Wage"]) * 52 + int(df.loc[df["ID"] == player, "Value"])
            if player_cost > max_price + residual_cash or player_cost == 0:
                continue
            else:
                attribute_count = 0
                for attribute in top11_values[position]:
                    if (player_has_NaN) or (attribute in ["ID", "Value", "Wage"]) or (math.isnan(df.loc[df["ID"] == player, attribute])):
                        player_has_NaN = True
                        continue
                    else:
                        attribute_count += 1
                        player_attribute_value = float(df.loc[df["ID"] == player, attribute])
                        ideal_attribute_value = ideal_stats.get(attribute)
                        difference = abs(player_attribute_value - ideal_attribute_value)
                        sum_difference += difference
            if player_has_NaN == False:
                if player not in used_player_list:
                    sum_difference_average = sum_difference / attribute_count
                    potential_player = [player, str(df.loc[df["ID"] == player, "Name"].values[0]), sum_difference_average, player_cost]
                    if player_chosen == []:
                        player_chosen = potential_player
                    elif potential_player[2] < player_chosen[2]:
                        player_chosen = potential_player
            else:
                continue 
        residual_cash = max_price + residual_cash - player_chosen[3]
        used_player_list.append(player_chosen[0])
        spent += player_chosen[3]                
        team[position] = player_chosen
        print(position, player_chosen, residual_cash)
    procent_spent = spent*100 / budget
    return team, spent, procent_spent


pprint.pprint(find_best_team(splitting_key = splitting_key(), players= eligible_players_list(), ideal_stats_to_pos= ideal_attributes(), top11_values = top11(ideal_attributes())))

