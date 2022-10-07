
formation = {
    "position1": ["1","2","3","4"]}

attribut_liste = ["skud","defense","passing"]


ideel_spiller_attributter = {}
ideel_spiller_dict = {}

for position in formation:
    ideel_spiller_attributter.clear()
    holdliste = formation.get(position)
    for attribut in attribut_liste:
        total_attribut_vaerdi = 0
        for spiller in holdliste:
            værdi = df.loc[df["ID"] == spiller, attribut][0]

            total_attribut_vaerdi += værdi
        attribut_gennemsnit= total_attribut_vaerdi/len(holdliste)
        ideel_spiller_attributter[attribut] = attribut_gennemsnit
    ideel_spiller_dict[position] = ideel_spiller_attributter

print(ideel_spiller_dict)

    
s