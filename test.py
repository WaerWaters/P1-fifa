import pandas as pd

#Læser datasættet og erstatter specielle tegn som den ikke var istand til at indkode med orden "aaa"
df = pd.read_csv('data.csv', encoding='UTF-8')
df=df.replace('\ufffd','aaa',regex=True)

#Finder navne med specielle karakterer og fremviser dem
def names_with_special_characters():
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        count = 0
        names = []
        for x in df.Name:
            if "aaa" in x:
                names.append(x)
                count += 1   
        print(count)
        print(names)


#Tjekker hvorvidt alle værdiger under "Value" er den samme valuta
def check_valuta():
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        count = 0
        for x in df.Value:
            if "€" in x:
                count += 1   
        print(count)

#Tjekker data typerne på hver colonne
def check_datatypes():
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df.dtypes)

check_datatypes()

#Kan tjekke hvor mange spillere hver position har
def check_quantity_position():
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        positions = ["RES", "SUB", "GK", "NaN"]
        count_res = 0
        count_sub = 0
        count_gk = 0
        count_nan = 0
        for x in df.Position:
            if positions[0] in str(x):
                count_res += 1
            elif positions[1] in str(x):
                count_sub += 1
            elif positions[2] in str(x):
                count_gk += 1
            else:
                count_nan += 1
        print("RES: " + str(count_res))
        print("SUB: " + str(count_sub))
        print("GK: " + str(count_gk))
        print("NaN: " + str(count_nan))
        print(count_gk + count_nan + count_res + count_sub)


