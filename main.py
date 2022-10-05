import pandas as pd

#Reads the data set and replace special characters that the encoding is unable to decode with the word "aaa"
df = pd.read_csv('data.csv', encoding='UTF-8')
df=df.replace('\ufffd','aaa',regex=True)

#Finding the names with the special characters and displaying them
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    count = 0
    names = []
    for x in df.Name:
        if "aaa" in x:
            names.append(x)
            count += 1   
    print(count)
    print(names)




