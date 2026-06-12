import pandas as pd

df_events = pd.read_csv("data/events.csv")

#Guaradmos las sesiones
sessions = df_events[df_events["event"] == "app_opened"]

#Sesiones por usuario
sessions_per_user = (sessions.groupby("user_id").size())

#Cruzarlo con usuarios
df_users = pd.read_csv("data/users.csv")

sessions_per_user = sessions_per_user.reset_index()

df = pd.merge(
    sessions_per_user,
    df_users,
    on="user_id"
)


df.groupby("plan")[0].mean()