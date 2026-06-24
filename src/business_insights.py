import pandas as pd 

# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================
#
# Objetivo:
# Obtener métricas e insights de negocio a partir de los
# usuarios y eventos generados en la simulación fintech.
#
# Preguntas:
#
# - ¿Cuántos usuarios hay?
# - ¿Qué porcentaje deposita dinero?
# - ¿Qué porcentaje empieza a invertir?
# - ¿Cuál es el depósito medio?
# - ¿Qué canal trae mejores usuarios?
# - ¿Qué plan convierte más rápido?
# - ¿Qué plan genera más inversores?
# - ¿Qué ocupación invierte más?
# - ¿Qué plan genera más dinero?
# - ¿Cuál es el segmento más valioso?
#
# ==========================================================

# ----------------------------------------------------------
# Cargar datasets
# ----------------------------------------------------------
df_users = pd.read_csv("data/users.csv")
df_events = pd.read_csv("data/events.csv")

df_events["timestamp"] = pd.to_datetime(df_events["timestamp"])

print("=== BUSINESS INSIGHTS ===\n")

# ----------------------------------------------------------
# Número total de usuarios
# ----------------------------------------------------------

total_users = len(df_users)
print(f"Total Users: {total_users}")

# ----------------------------------------------------------
# Conversión Signup -> Deposit
# ----------------------------------------------------------
event_counts = df_events["event"].value_counts()

#Contar cuantas veces ocurre cada evento
sign_up = event_counts["sign_up"]
deposit = event_counts["first_deposit"]

#Tasa de conversión
deposit_conversion = (deposit/sign_up)*100

print(
    f"Signup -> Deposit Conversion: "
    f"{deposit_conversion:.2f}%"
)

# ----------------------------------------------------------
# Conversión Signup -> Investment
# ----------------------------------------------------------
#Contar cuanta gente empezó a invertir
investment = event_counts["investment_started"]

#Tasa de conversión
investment_conversion = (investment/sign_up)*100

print(
    f"Signup -> Investment Conversion: "
    f"{investment_conversion:.2f}%"
)

# ----------------------------------------------------------
# Depósito medio
# ----------------------------------------------------------
#Obtenemos los depositos
deposits = df_events[df_events["event"] == "first_deposit"]

#Mediia de los depositos
average_deposit = (deposits["deposit_amount"].mean())

print(
    f"Average Deposit Amount: "
    f"€{average_deposit:.2f}"
)

# ----------------------------------------------------------
# Usuarios inversores
# ----------------------------------------------------------
#Obtener que usuarios son inversores y marcarlos con True
investors = df_events[df_events["event"] == "investment_started"][["user_id"]]
investors["is_investor"] = True

df = pd.merge(df_users,investors, on = "user_id", how="left")

df["is_investor"] = (df["is_investor"].fillna(False))

# ----------------------------------------------------------
# Mejor canal de adquisición
# ----------------------------------------------------------

#Tasa de conversion por canal 
channel_conversion = (df.groupby("acquisition_channel")["is_investor"].mean()*100)
#Mejor canal 
best_channel = (channel_conversion.idxmax())
#Canal con mayor tasa
best_channel_rate = (channel_conversion.max())

print()
print("Best Acquisition Channel:")
print(
    f"{best_channel} "
    f"({best_channel_rate:.2f}%)"
)

# ----------------------------------------------------------
# Plan que convierte más rápido a depósito
# ----------------------------------------------------------

#Personas que hacen signup
signup_df = df_events[df_events["event"] == "sign_up"][["user_id", "timestamp"]]

#Personas que hacen deposit
deposit_df = df_events[df_events["event"] == "first_deposit"][["user_id", "timestamp"]]

#Cmabiar el nombre de las columnas
signup_df = signup_df.rename(columns={"timestamp":"signup_date"})
deposit_df = deposit_df.rename(columns={"timestamp":"deposit_date"})

#Merge de ambos dataframes
time_df = pd.merge(signup_df, deposit_df, on="user_id")

#Calculo de dias que el usuario tardo en depositar 
time_df["days_to_deposit"] = (time_df["deposit_date"]-time_df["signup_date"]).dt.days

#Merge con la tabal usuarios
time_df = pd.merge(time_df, df_users[["user_id", "plan"]], on="user_id")

#Velocidad de conversión para cada plan
plan_speed = (time_df.groupby("plan")["days_to_deposit"].mean())

#El plan que conviert más rápido es que tiene la media mas baja
fastest_plan = (plan_speed.idxmin())
fastest_days = (plan_speed.min())

print()
print("Fastest Converting Plan:")
print(
    f"{fastest_plan} "
    f"({fastest_days:.2f} days)"
)

# ----------------------------------------------------------
# Plan con mayor tasa de inversión
# ----------------------------------------------------------

#Tasa de conversion
plan_conversion = (df.groupby("plan")["is_investor"].mean()*100)

#Mejor plan y tasa 
best_plan = (plan_conversion.idxmax())
best_plan_rate = (plan_conversion.max())

print()
print("Best Investment Plan:")
print(
    f"{best_plan} "
    f"({best_plan_rate:.2f}%)"
)

# ----------------------------------------------------------
# Ocupación con mayor tasa de inversión
# ----------------------------------------------------------

#Tasa de conversionn
occupation_conversion = (df.groupby("occupation")["is_investor"].mean()*100)

#Ocupacion con mayor tasa y su tasa
best_occupation = (occupation_conversion.idxmax())
best_occupation_rate = (occupation_conversion.max())

print()
print("Best Investor Occupation:")
print(
    f"{best_occupation} "
    f"({best_occupation_rate:.2f}%)"
)

# ----------------------------------------------------------
# Plan que genera más dinero
# ----------------------------------------------------------

#Merge de deposios y usuarios
deposit_plan_df = pd.merge(deposits,df_users[["user_id", "plan"]], on="user_id")

#Ganancia por plan
revenue_by_plan = (deposit_plan_df.groupby("plan")["deposit_amount"].sum())

#Mejor plan y su revenue
top_plan = (revenue_by_plan.idxmax())
top_revenue = revenue_by_plan.max()

print()
print("Highest Revenue Plan:")

print(
    f"{top_plan} "
    f"(€{top_revenue:.2f})"
)

# ----------------------------------------------------------
# Segmento con mayor conversión a inversión
# ----------------------------------------------------------

#Tasa de conversion
segment_conversion = (df.groupby(["country","occupation"])["is_investor"].mean()*100)

#Mejor segemento y tasa
best_segment = (segment_conversion.idxmax())
best_segment_rate = (segment_conversion.max())

print()
print("Top Investor Segment:")
print(
    f"{best_segment[0]} - "
    f"{best_segment[1]} "
    f"({best_segment_rate:.2f}%)"
)

# ----------------------------------------------------------
# Insight automático
# ----------------------------------------------------------
print()
print("=== KEY INSIGHTS ===")

print(
    f"- {best_channel} is the best acquisition channel."
)

print(
    f"- {best_plan} users have the highest investment rate."
)

print(
    f"- {best_occupation} users invest more frequently."
)

print(
    f"- {top_plan} generates the highest deposit volume."
)