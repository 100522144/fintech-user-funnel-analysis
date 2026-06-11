import pandas as pd
import random

#Posibles paises del usuario
countries = [
    "Spain",
    "Portugal",
    "UK",
    "Germany",
    "France",
    "Poland"
]

#Posibles dispositivos del usuario
devices = [
    "Android",
    "iPhone"
]

#Posibles ocupaciones del usuario
occupations = [
    "Student",
    "Employee",
    "Self-employed"
]

#Posibles canales por los que conoció la plataforma
channels = [
    "TikTok",
    "Instagram",
    "Google",
    "Referral",
    "YouTube"
]


#Funcion para generar un usuario

def generate_user(user_id):

    #Campos del usuario
    country = random.choice(countries)
    device = random.choice(devices)
    occupation = random.choice(occupations)
    #La edad se decide en función de la ocupación
    if occupation == "Student":
        age = random.randint(18,24)
    elif occupation == "Employee":
        age = random.randint(22,65)
    else:
        age = random.randint(25,65)
    channel = random.choice(channels)

    return {
        "user_id": user_id,
        "age": age,
        "country": country,
        "device": device, 
        "occupation": occupation, 
        "acquisition_channel": channel 
    }

users = []

for i in range(1,101):

    user = generate_user(i)
    users.append(user)

#Hacer dataframe de usuarios
df_users = pd.DataFrame(users)

print(df_users.head())