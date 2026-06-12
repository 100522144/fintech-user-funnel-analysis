import pandas as pd

#Datafra,e de suer y evnetos
df_users = pd.read_csv("data/users.csv")
df_events = pd.read_csv("data/events.csv")

#Unir las dos tablas para tenerlo en una sola
df = pd.merge(df_events, df_users, on="user_id")

#Crear una nueva columan booleana
df["is_investor"] = df["event"] == "investment_started"

#Agrupar por dispistivo
print(df.groupby("device")["is_investor"].sum())


#Calcular usuarios por dispoistivo
print(df_users["device"].value_counts())


#Analisis:Quienes invierten

#Seleccionamos solo los inversores
investors = df[df["event"] == "investment_started"]
#Pais de los inversores
print(investors["country"].value_counts())
#Dispositivos de los inversores
print(
    investors["device"].value_counts()
)
#A que se dedican los inversores
print(investors["occupation"].value_counts())


#Calcular tasa de inversión por ocupación
total_by_occupation = df_users["occupation"].value_counts()

investors_by_occupation = investors["occupation"].value_counts()

print("Total usuarios")
print(total_by_occupation)

print()
print("Usuarios inversores")
print(investors_by_occupation)

for occupation in total_by_occupation.index:

    total = total_by_occupation[occupation]
    investors_count = investors_by_occupation.get(occupation,0)
    rate = (investors_count/total)*100
    print(f"{occupation}: {rate:.2f}%")

#Calcular la tasa de inversores por plan
total_by_plan = df_users["plan"].value_counts()
investors_by_plan = investors["plan"].value_counts()

for plan in total_by_plan.index:

    total_plan = total_by_plan[plan]
    total_investors = investors_by_plan.get(plan,0)
    rate = (total_investors/total_plan)*100
    print(f"{plan}: {rate:.2f}%")