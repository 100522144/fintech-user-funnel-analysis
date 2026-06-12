import pandas as pd

#Leer el csv 
df_users = pd.read_csv("data/users.csv")
df_events = pd.read_csv("data/events.csv")

#Bucle para contar la tasa de converion entre los que se registran y otros eeventos
#De esta forma se puede saber cuantos usuarios llegan hasta que paso
event_counts = df_events["event"].value_counts()
signup = event_counts["sign_up"]
for event, count in event_counts.items():
    conversion = (count/signup)*100
    print(f"{event}: {count} users ({conversion:.2f}%)")


#Como poder ver donde se pierden los clientes entre difernetes pasos

funnel_steps = [
    "sign_up",
    "kyc_completed",
    "first_deposit",
    "card_ordered",
    "first_payment",
    "investment_started"
]

for i in range(len(funnel_steps)-1):
    #Obentenemos el paso en que esta y el siguiente
    current_step = funnel_steps[i]
    next_step = funnel_steps[i+1]
    #Contamos los valores para estos pasos
    current_count = event_counts[current_step]
    next_count = event_counts[next_step]
    #Calculamos el porcenatje de conversion

    conversion = (next_count/current_count)*100

    print(
        f"{current_step} -> {next_step}: "
        f"{conversion:.2f}%"
    )
