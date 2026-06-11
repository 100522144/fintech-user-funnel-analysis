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