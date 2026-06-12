import pandas as pd

#Dataframe de los eventos
df_events = pd.read_csv("data/events.csv")

#Convertir la fecha a tipo date
df_events["timestamp"] = pd.to_datetime(df_events["timestamp"])

#Seprar el evento sign up y deposit

signup = df_events[
    df_events["event"] == "sign_up"
][["user_id", "timestamp"]]

deposit = df_events[
    df_events["event"] == "first_deposit"
][["user_id", "timestamp"]]

#Renombrar las columnas
signup = signup.rename(columns={"timestamp": "signup_date"})
deposit = deposit.rename(columns={"timestamp": "deposit_date"})

#JOIN
df = pd.merge(signup,deposit,on="user_id")

#Calcular dias que pasan entre deposito y signup
df["days_to_deposit"] = (df["deposit_date"]-df["signup_date"]).dt.days

print(
    df["days_to_deposit"].describe()
)

df_users = pd.read_csv("data/users.csv")

df = pd.merge(df,df_users, on="user_id")
print(
    df.groupby("plan")["days_to_deposit"].mean()
)