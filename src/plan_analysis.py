import pandas as pd

#Dataframes de users y events

df_users = pd.read_csv("data/users.csv")
df_events = pd.read_csv("data/events.csv")

#Calcular el numero de usuarios que inviertieron
investors = df_events[df_events["event"] == "investment_started"]["user_id"].unique()

#Nueva columna
df_users["is_investor"] = df_users["user_id"].isin(investors)

#Tasa por plan
plan_conversion = df_users.groupby("plan")["is_investor"].mean()*100

print("Investment rate by plan")
print(plan_conversion)

#Calcular el deposito medio por plan
deposits = df_events[df_events["event"] == "first_deposit"]

df = deposits.merge(
    df_users[["user_id","plan"]],
    on="user_id"
)

avg_deposit = (df.groupby("plan")["deposit_amount"].mean())

print("\nAverage deposit by plan")
print(avg_deposit)

#Plan más popular
print("\nUsers by plan")

print(
    df_users["plan"]
    .value_counts()
)

#Mejor plan 
best_plan = plan_conversion.idxmax()

print(
    f"\nInsight: {best_plan} has the highest investment conversion rate."
)
