import pandas as pd

#Cargar los datos
df_users = pd.read_csv("data/users.csv")
df_events = pd.read_csv("data/events.csv")

#Crear la tabla inversores
investors = df_events[df_events["event"] == "investment_started"]

#Coger solo el user_id
investors = investors[["user_id"]]

#Añadir nueva columna bool is investor
investors["is_investor"] = True

#Hacer join con usuarios
df = pd.merge(df_users,investors,on="user_id", how="left")

#Convertir los NaN a False
df["is_investor"] = df["is_investor"].fillna(False)

#Calcular la tasa de inversión por canal
result = df.groupby("acquisition_channel")["is_investor"].mean()*100

print(result)