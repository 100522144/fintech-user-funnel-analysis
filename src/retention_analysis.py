import pandas as pd

df_events = pd.read_csv("data/events.csv")

#Convertirlo a date
df_events["timestamp"] = pd.to_datetime(df_events["timestamp"])

#Quedarnos con los sign up

signup = df_events[df_events["event"] == "sign_up"][["user_id", "timestamp"]]

#Renombrar la columna
signup = signup.rename(columns={"timestamp":"signup_date"})

#Coger las que son solo aperturas de app
sessions = df_events[df_events["event"] == "app_opened"][["user_id", "timestamp"]]

#Hacer join

df = pd.merge(sessions, signup, on="user_id")
print(df.head())

#Calculo de dias desde registro
df["days_since_signup"] = (df["timestamp"]-df["signup_date"]).dt.days

#Calcular los usuarios retenidos en D7
retained_d7 = df[df["days_since_signup"]>=7]
retained_users_d7 = retained_d7["user_id"].nunique()

#Tasa de D7
total_users = signup["user_id"].nunique()
d7_rate = (
    retained_users_d7
    /
    total_users
) * 100

print(f"D7 Retention: {d7_rate:.2f}%")

#Retención a 30 días
retained_d30 = df[df["days_since_signup"]>=30]
retained_users_d30 = retained_d30["user_id"].nunique()

#Tasa de D30
total_users = signup["user_id"].nunique()
d30_rate = (
    retained_users_d30
    /
    total_users
) * 100

print(f"D30 Retention: {d30_rate:.2f}%")


#Retencion por plan 
df_users = pd.read_csv("data/users.csv")

retained_d30_users = retained_d30[["user_id"]].drop_duplicates()
retained_d30_users["retained"] = True

df_retention = pd.merge(df_users, retained_d30_users, on="user_id", how="left")
df_retention["retained"] = (
    df_retention["retained"]
    .fillna(False)
)

print(df_retention.groupby("plan")["retained"].mean() * 100)