import pandas as pd
import random
from datetime import datetime, timedelta

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

plans = [
    "Basic",
    "Plus",
    "Pro",
    "Elite"
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
    registration_date = datetime(
        2025, 
        random.randint(1,12),
        random.randint(1,28)
    )
    plan = random.choices(plans, weights = [60,25,10,5],k=1)[0]
    return {
        "user_id": user_id,
        "age": age,
        "country": country,
        "device": device, 
        "occupation": occupation, 
        "acquisition_channel": channel,
        "income_level": income_level,
        "registration_date": registration_date,
        "plan": plan
    }


def generate_events(user):
    #Funcion que va a genear los eventos de un usuario
    user_id = user["user_id"]
    registration_date = user["registration_date"]
    occupation = user["occupation"]
    income_level = user["income_level"]
    plan = user["plan"]
    
    events = []

    #Todos los usuarios hacen signup
    events.append({"user_id": user_id,
                   "event": "sign_up",
                   "timestamp": registration_date})
    
    #Aprox el 80% van a completar el kyc
    if random.random() < 0.8:
        #Fecha para el kyc
        kyc_date = registration_date + timedelta(days=random.randint(0,2))

        events.append({"user_id": user_id, 
                       "event": "kyc_completed",
                       "timestamp": kyc_date
                       })
        
        #En el deposito se va a añadir una cantidad de dinero aletaroria
        # en funcion de los ingresos de cada usuario
        deposit_amount = round(income_level*random.uniform(0.05,0.30),2)
    
        #Aprox el 75% va a hacer un deposito luego de completar el kyc
        if random.random() < 0.75:
            #Fecha del deposito
            deposit_date = kyc_date + timedelta(days = random.randint(1,7))
            events.append({
                "user_id": user_id,
                "event": "first_deposit",
                "timestamp": deposit_date,
                "deposit_amount": deposit_amount
            })
        
            #El 85% de esos usuarios acabara pidiendo una tarjeta
            if random.random() < 0.85:
                #Feecha para tarjeta
                card_date = deposit_date + timedelta(days = random.randint(1,5))
                events.append({
                    "user_id": user_id,
                    "event": "card_ordered",
                    "timestamp": card_date
                })

                #Despues el 80% hara un pago 
                if random.random() < 0.8:
                    #Fecha del primer pago
                    payment_date = card_date + timedelta(days = random.randint(1,15))

                    events.append({
                        "user_id": user_id,
                        "event": "first_payment",
                        "timestamp": payment_date
                    })

                    #Probabilidad de inversión en función del plan del usuario
                    if plan == "Elite":
                        investment_probability = 0.70
                    elif plan == "Pro":
                        investment_probability = 0.50
                    elif plan == "Plus":
                        investment_probability = 0.35
                    else:
                        investment_probability = 0.20
                    #El 35% hará una inversión
                    if random.random() < investment_probability:
                        #Fecha primera inversión
                        investment_date = payment_date + timedelta(days = random.randint(5,90))
                        events.append({
                            "user_id": user_id,
                            "event": "investment_started",
                            "timestamp": investment_date
                        })

    
    return events


#Crear los usuarios
users = []
for i in range(1,101):
    user = generate_user(i)
    users.append(user)

#Crear eventos
all_events = []
for user in users:
    user_events = generate_events(user)
    all_events.extend(user_events)

#Crear dataframes
df_users = pd.DataFrame(users)
df_events = pd.DataFrame(all_events)

df_users.to_csv("data/users.csv", index=False)
df_events.to_csv("data/events.csv", index=False)
