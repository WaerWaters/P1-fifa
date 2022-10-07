from enum import unique



def vaegtet_differens(tal1,tal2,vaegtning):# regner den numeriske værdi af en differens mellem to tal med en vægtning ganget på 
    # tal1 og tal2 er tallene der sammenlignes.
    vaegtet_differens_tal = abs(tal1-tal2)*vaegtning
    return vaegtet_differens_tal





formation_dict = { #dict over de forskellige formationer, nok ikke vigtigt da vi kan tage dirkete fra formationen istedetfor.
    "4-4-2": {"position1": 0, #nulværdien skal være et nyt dictionary over attributterne for de ideeler spiller i den position
             "position2": 0}#bare et eksempel på hvordan formationen skal opbygges hver punkt skal være: position: 0
                            # det skal bruges til at lave en liste over ideele spiller i senere i beregningerne, til 
                            # værdi ideelle_spiller.
    "4-3-3":[] , 
    "4-2-3-1":[] ,
}    
postioner =["liste over alle postioner"]

def find_spiller_til(fordelingsnoegle, formation, budget,spillerliste):
    ny_spillere = {}
    ideel_spiller_dict = formation_dict.get(formation) #sætter ideelle_spiller til at være lig en dict som ligner formationen.
    for position in formation: #starter ud med at kigge på hver position i formationen
        ideel_spiller_til_position = ideel_spiller_dict.get(position) # tager den ideele spiller i den postion og sætter den lig en værdi
        sum_differens = 0.
        for spiller in spillerliste: # starter søgningen efter spillere i spillerlisten.
            maksimalpris = budget * fordelingsnoegle[position]
            if spiller.get("value") > maksimalpris:
                pass # mangler kommanden til at hopper over den her iteration af forloopen for spiller in spillerliste
            elif True:
                antal_attributter = 0
                for attribut in spiller: # beregner diffen for hver attribut for spilleren, ift. den ideele i den position.
                    antal_attributter += 1
                    spiller_attribut_vaerdi = spiller.get(attribut)
                    ideel_attribut_vaerdi = ideel_spiller_til_position.get(attribut) 

                    vaegtet_differens(spiller_attribut_vaerdi,ideel_attribut_vaerdi,1) #finder differensen med en vægtning på 1. 
                    sum_differens += vaegtet_differens
            sum_differens_gennemsnit = sum_differens / antal_attributter
            
            if ny_spillere.get(position) == None:
                ny_spillere[position] = [spiller.get(ID),sum_differens_gennemsnit]
            else:
                Spiller_værdisæt = ny_spillere[position]

                if sum_differens_gennemsnit < Spiller_værdisæt[1]:
                    ny_spillere[position] = [spiller.get(ID),sum_differens_gennemsnit]
    return ny_spillere

                




formation_positioner_4_4_2 = [] # hvad for nogle postioner indgår i formationen i form af en liste eller tuple
formation_positioner_4_3_3 = []
formation_positioner_4_2_3_1 = []

alle_positioner_i_bedste_positioner = ["CAM", "CB", "CDM", "CF", "CM","GK","LB","LM","LW","LWB","RB","RM","RW","RWB","ST"]
alle_positioner_i_positioner = ["GK", "CDM", "LDM", "RM", "RCM", "CM", "LCM","LM","RAM","CAM","LAM","RWB","RF","CF","LF","RW","RS","ST","LS","LW","SUB","RES","RB","RCB","CB","LCB","LB","LWB","RDM"]








print(thisdict["brand"])