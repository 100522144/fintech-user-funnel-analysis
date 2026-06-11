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
        income_level = random.randint(300,1200)
    elif occupation == "Employee":
        age = random.randint(22,65)
        income_level = random.randint(1200,6000)
    else:
        age = random.randint(25,65)
        income_level = random.randint(1000,10000)
    channel = random.choice(channels)

    return {
        "user_id": user_id,
        "age": age,
        "country": country,
        "device": device, 
        "occupation": occupation, 
        "acquisition_channel": channel,
        "income_level": income_level
    }


def generate_events(user_id):
    #Funcion que va a genear los eventos de un usuario
    events = []

    #Todos los usuarios hacen signup
    events.append({"user_id": user_id,
                   "event": "sign_up"})
    
    #Aprox el 80% van a completar el kyc
    if random.random() < 0.8:
        events.append({"user_id": user_id, 
                       "event": "kyc_completed"})
    
        #Aprox el 75% va a hacer un deposito luego de completar el kyc
        if random.random() < 0.75:
            events.append({
                "user_id": user_id,
                "event": "first_deposit"
            })
        
            #El 85% de esos usuarios acabara pidiendo una tarjeta
            if random.random() < 0.85:

                events.append({
                    "user_id": user_id,
                    "event": "card_ordered"
                })

                #Despues el 80% hara un pago 
                if random.random() < 0.8:

                    events.append({
                        "user_id": user_id,
                        "event": "first_payment"
                    })

                    #El 35% hará una inversión
                    if random.random() < 0.35:

                        events.append({
                            "user_id": user_id,
                            "event": "investment_started"
                        })

    
    return events


#Crear los usuarios
users = []
for i in range(1,101):
    user = generate_user(i)
    users.append(user)

#Crear eventos
all_events = []
for i in range(1,101):
    user_events = generate_events(i)
    all_events.extend(user_events)

#Crear dataframes
df_users = pd.DataFrame(users)
df_events = pd.DataFrame(all_events)

df_users.to_csv("data/users.csv", index=False)
df_events.to_csv("data/events.csv", index=False)
