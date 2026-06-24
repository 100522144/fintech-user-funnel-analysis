import pandas as pd

# ==========================================================
# TIME ANALYSIS
# ==========================================================
#
# Objetivo:
# Analizar el tiempo que tardan los usuarios en realizar
# su primer depósito tras registrarse.
#
# Preguntas:
#
# - ¿Cuánto tarda un usuario en depositar?
# - ¿Qué plan convierte más rápido?
# - ¿Qué ocupación convierte más rápido?
# - ¿Qué país convierte más rápido?
# - ¿Cuáles son los usuarios más rápidos?
#
# ==========================================================


# ----------------------------------------------------------
# Cargar datasets
# ----------------------------------------------------------

df_events = pd.read_csv("data/events.csv")
df_users = pd.read_csv("data/users.csv")

#Convertir timestamp a fecha
df_events["timestamp"] = pd.to_datetime(df_events["timestamp"])

# ----------------------------------------------------------
# Obtener registros y depósitos
# ----------------------------------------------------------

#Obetener los datos
signup = df_events[df_events["event"] == "sign_up"][["user_id", "timestamp"]]
deposit = df_events[df_events["event"] == "first_deposit"][["user_id", "timestamp"]]

#Renombrar columnas
signup = signup.rename(columns={"timestamp": "signup_date"})
deposit = deposit.rename(columns={"timestamp":"deposit_date"})

#Merge de regitsros y depositos
df = pd.merge(signup,deposit, on="user_id")

# ----------------------------------------------------------
# Calcular días hasta el depósito
# ----------------------------------------------------------

#Dias que pasan desde que se registran hasta que hace un depósito
df["days_to_deposit"] = (df["deposit_date"]-df["signup_date"]).dt.days

# ----------------------------------------------------------
# Estadísticas generales
# ----------------------------------------------------------

print("=== TIME ANALYSIS ===\n")

print("Days to Deposit Summary:\n")

print(
    df["days_to_deposit"]
    .describe()
)

# ----------------------------------------------------------
# Añadir información de usuario
# ----------------------------------------------------------

#Merge con los usuarios
df = pd.merge(df, df_users, on="user_id")

# ----------------------------------------------------------
# Tiempo medio por plan
# ----------------------------------------------------------
print("\n=== AVERAGE DAYS TO DEPOSIT BY PLAN ===\n")

plan_speed = (df.groupby("plan")["days_to_deposit"].mean())

print(plan_speed.sort_values())

# ----------------------------------------------------------
# Tiempo medio por ocupación
# ----------------------------------------------------------

print("\n=== AVERAGE DAYS TO DEPOSIT BY OCCUPATION ===\n")

ocupation_speed = (df.groupby("occupation")["days_to_deposit"].mean())

print(ocupation_speed.sort_values())

# ----------------------------------------------------------
# Tiempo medio por país
# ----------------------------------------------------------

print("\n=== AVERAGE DAYS TO DEPOSIT BY COUNTRY ===\n")

country_speed = (df.groupby("country")["days_to_deposit"].mean())

print(country_speed.sort_values())

# ----------------------------------------------------------
# Usuarios más rápidos
# ----------------------------------------------------------

print("\n=== FASTEST USERS ===\n")

#Ordenar los usuarios y coger los 10 primeros
fastest_users = (df.sort_values(by="days_to_deposit").head(10))

#Mostrar los datos de ese usuario
print(fastest_users[["user_id", "days_to_deposit", "plan", "occupation", "country"]])

# ----------------------------------------------------------
# Usuarios más lentos
# ----------------------------------------------------------

print("\n=== SLOWEST USERS ===\n")

#Ordenar los usuarios al revés y coger los 10 primeros
slowest_users = (df.sort_values(by="days_to_deposit", ascending=False).head(10))

#Mostrar los datos de ese usuario
print(slowest_users[["user_id", "days_to_deposit", "plan", "occupation", "country"]])

# ----------------------------------------------------------
# Plan más rápido
# ----------------------------------------------------------

#Plan más rápido y sus dias
fastest_plan =(plan_speed.idxmin())
fastest_days = (plan_speed.min())

print("\n=== FASTEST PLAN ===\n")

print(
    f"{fastest_plan} "
    f"({fastest_days:.2f} days)"
)

# ----------------------------------------------------------
# Insight automático
# ----------------------------------------------------------

print("\n=== KEY INSIGHTS ===\n")

print(
    f"- Users need an average of "
    f"{df['days_to_deposit'].mean():.2f} days "
    f"to complete their first deposit."
)

print(
    f"- {fastest_plan} users convert faster "
    f"than any other plan."
)



