import pandas as pd


# ==========================================================
# ACTIVITY ANALYSIS
# ==========================================================
#
# Objetivo:
# Analizar el nivel de actividad de los usuarios dentro
# de la aplicación a partir de los eventos "app_opened".
#
# Preguntas:
#
# - ¿Qué planes utilizan más la aplicación?
# - ¿Qué ocupaciones son más activas?
# - ¿Qué países muestran mayor engagement?
# - ¿Qué canales atraen usuarios más activos?
# - ¿Los usuarios que invierten usan más la app?
# - ¿Quiénes son los usuarios más activos?
#
# ==========================================================

# ----------------------------------------------------------
# Cargar datasets
# ----------------------------------------------------------

df_events = pd.read_csv("data/events.csv")
df_users = pd.read_csv("data/users.csv")

# ----------------------------------------------------------
# Filtrar aperturas de la aplicación
# ----------------------------------------------------------

#Solamente intersan los eventos que represntan apertura de app
sessions = df_events[df_events["event"] == "app_opened"]

# ----------------------------------------------------------
# Calcular número de sesiones por usuario
# ----------------------------------------------------------

#Agrupar por usuario y contar cuantas aperturas ha hecho
sessions_per_user = (sessions.groupby("user_id").size().reset_index())

#Renombrar las columnas
sessions_per_user.columns = ["user_id", "sessions"]

# ----------------------------------------------------------
# Unir sesiones con información de usuarios
# ----------------------------------------------------------

df = pd.merge(sessions_per_user, df_users, on ="user_id")

# ----------------------------------------------------------
# Actividad media por plan
# ----------------------------------------------------------

print("\n=== Average Sessions by Plan ===")
print(df.groupby("plan")["sessions"].mean().sort_values(ascending=False))

# ----------------------------------------------------------
# Actividad media por ocupación
# ----------------------------------------------------------

print("\n=== Average Sessions by Occupation ===")
print(df.groupby("occupation")["sessions"].mean().sort_values(ascending=False))

# ----------------------------------------------------------
# Actividad media por país
# ----------------------------------------------------------

print("\n=== Average Sessions by Country ===")
print(df.groupby("country")["sessions"].mean().sort_values(ascending = False))

# ----------------------------------------------------------
# Actividad media por canal de adquisición
# ----------------------------------------------------------

print("\n=== Average Sessions by Acquisition Channel ===")
print(df.groupby("acquisition_channel")["sessions"].mean().sort_values(ascending=False))

# ----------------------------------------------------------
# Usuarios más activos
# ----------------------------------------------------------

print("\n=== Top 10 Most Active Users ===")
top_users = (df.sort_values(by="sessions", ascending=False).head(10))
print(top_users[["user_id", "sessions", "plan", "occupation", "country"]])

# ----------------------------------------------------------
# Comparar actividad entre inversores y no inversores
# ----------------------------------------------------------

#Obetner que usuarios han hecho una inversión
investors = df_events[df_events["event"] == "investment_started"]["user_id"].unique()

#Variable bool que determina si es inversor o no
df["is_investor"] = (df["user_id"].isin(investors))

#Mostrar la información
print("\n=== Investor vs Non-Investor Activity ===")
print(df.groupby("is_investor")["sessions"].mean())

# ----------------------------------------------------------
# Estadísticas de actividad por plan
# ----------------------------------------------------------

print("\n=== Activity Distribution by Plan ===")
activity_stats = (df.groupby("plan")["sessions"].agg(["mean", "min", "max", "median"]))
print(activity_stats)

# ----------------------------------------------------------
# Insight automático
# ----------------------------------------------------------

most_active_plan = (df.groupby("plan")["sessions"].mean().idxmax())
print( f"\nInsight: {most_active_plan} users show the highest average activity.")