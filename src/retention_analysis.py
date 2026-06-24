import pandas as pd

# ==========================================================
# RETENTION ANALYSIS
# ==========================================================
#
# Objetivo:
# Analizar cuántos usuarios siguen utilizando la aplicación
# después de registrarse.
#
# Métricas:
#
# - D7 Retention
# - D30 Retention
# - Retention by Plan
# - Retention by Occupation
# - Retention by Country
# - Best Retained Segment
# - Investor vs Non-Investor Retention
#
# ==========================================================

# ----------------------------------------------------------
# Cargar datasets
# ----------------------------------------------------------

df_users = pd.read_csv("data/users.csv")
df_events = pd.read_csv("data/events.csv")

#Convertir el tiempo a formato fecha
df_events["timestamp"] = pd.to_datetime(df_events["timestamp"])

# ----------------------------------------------------------
# Obtener fecha de registro de cada usuario
# ----------------------------------------------------------

#Fecha del usuario
signup = df_events[df_events["event"] == "sign_up"][["user_id", "timestamp"]]

#Renombrar la columna
signup = signup.rename(columns={"timestamp":"signup_date"})

# ----------------------------------------------------------
# Obtener aperturas de aplicación
# ----------------------------------------------------------

#Eventos de apertura de app
sessions = df_events[df_events["event"] == "app_opened"][["user_id", "timestamp"]]

# ----------------------------------------------------------
# Relacionar sesiones con fecha de registro
# ----------------------------------------------------------

df = pd.merge(sessions, signup, on="user_id")

# ----------------------------------------------------------
# Calcular días desde registro
# ----------------------------------------------------------

df["days_since_signup"] = (df["timestamp"]-df["signup_date"]).dt.days

# ----------------------------------------------------------
# Retención D7
# ----------------------------------------------------------

#Usarios en D7
retained_d7 = df[df["days_since_signup"] >= 7]
retained_users_d7 = (retained_d7["user_id"].nunique())
total_users = (signup["user_id"].nunique())

#Tasa
d7_rate = (retained_users_d7/total_users)*100

print("=== RETENTION ANALYSIS ===\n")
print(
    f"D7 Retention: "
    f"{d7_rate:.2f}%"
)

# ----------------------------------------------------------
# Retención D30
# ----------------------------------------------------------

#Usarios en D30
retained_d30 = df[df["days_since_signup"] >= 30]
retained_users_d30 = (retained_d30["user_id"].nunique())
total_users = (signup["user_id"].nunique())

#Tasa
d30_rate = (retained_users_d30/total_users)*100

print(
    f"D30 Retention: "
    f"{d30_rate:.2f}%"
)

# ----------------------------------------------------------
# Crear dataset de retención
# ----------------------------------------------------------

retained_d30_users = (retained_d30[["user_id"]].drop_duplicates())
retained_d30_users["retained"] = True

#Merge de ambos df
df_retention = pd.merge(df_users,retained_d30_users,on="user_id", how="left")

#Poner los false
df_retention["retained"] = (df_retention["retained"].fillna(False))

# ----------------------------------------------------------
# Retención por plan
# ----------------------------------------------------------

print("\n=== D30 RETENTION BY PLAN ===\n")

plan_retention = (df_retention.groupby("plan")["retained"].mean()*100)

print(plan_retention.sort_values(ascending=False))



# ----------------------------------------------------------
# Retención por ocupación
# ----------------------------------------------------------

print("\n=== D30 RETENTION BY OCCUPATION ===\n")

occupation_retention = (df_retention.groupby("occupation")["retained"].mean()*100)
print(occupation_retention.sort_values(ascending=False))

# ----------------------------------------------------------
# Retención por país
# ----------------------------------------------------------

print("\n=== D30 RETENTION BY COUNTRY ===\n")

country_retention = (df_retention.groupby("country")["retained"].mean()*100)

print(country_retention.sort_values(ascending=False))

# ----------------------------------------------------------
# Mejor segmento retenido
# ----------------------------------------------------------

#Retencion por segmento
segment_retention = (df_retention.groupby(["country", "occupation"])["retained"].mean()*100)

#Mejor segmento y su tasa
best_segment = (segment_retention.idxmax())
best_segment_rate = (segment_retention.max())

print("\n=== BEST RETAINED SEGMENT ===\n")
print(
    f"{best_segment[0]} - "
    f"{best_segment[1]} "
    f"({best_segment_rate:.2f}%)"
)

# ----------------------------------------------------------
# Comparar inversores y no inversores
# ----------------------------------------------------------

#Sacar los usuarios que son inversores
investors = df_events[df_events["event"] == "investment_started"]["user_id"].unique()

#Retencion
df_retention["is_investor"] = (df_retention["user_id"].isin(investors))

print("\n=== INVESTOR VS NON-INVESTOR RETENTION ===\n")

#Retencion por inversores
investor_retention = (df_retention.groupby("is_investor")["retained"].mean()*100)

print(investor_retention)

# ----------------------------------------------------------
# Mejor plan retenido
# ----------------------------------------------------------

#Mejor plan y su tasa de retención
best_plan = (plan_retention.idxmax())
best_plan_rate = (plan_retention.max())

print("\n=== BEST RETAINED PLAN ===\n")
print(
    f"{best_plan} "
    f"({best_plan_rate:.2f}%)"
)

# ----------------------------------------------------------
# Insights automáticos
# ----------------------------------------------------------

print("\n=== KEY INSIGHTS ===\n")

print(
    f"- D30 retention is "
    f"{d30_rate:.2f}%."
)

print(
    f"- {best_plan} users show "
    f"the highest retention."
)

print(
    f"- {best_segment[0]} "
    f"{best_segment[1]} users "
    f"are the most loyal segment."
)
