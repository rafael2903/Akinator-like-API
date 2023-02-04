import pandas as pd
import random

# Cria uma lista vazia para armazenar os dados dos personagens
characters = []

# Gera os dados dos personagens
for i in range(500):
    characters.append({
        "É homem?": random.choice([1, -1]),
        "Tem mais de 170 de altura?": random.choice([1, -1]),
        "Nasceu depois da década de 80?": random.choice([1, -1]),
        "Pesa menos de 80 Kg?": random.choice([1, -1]),
        "É careca?": random.choice([1, -1]),
        "name": "Personagem " + str(i+1)
    })

# Cria um dataframe a partir da lista de personagens
df = pd.DataFrame(characters)

# Salva o dataframe em um arquivo Excel
# df.to_excel("characters.xlsx")
df.to_csv("characters.csv", index=False)
