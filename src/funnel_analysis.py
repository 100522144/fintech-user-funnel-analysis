
import pandas as pd

# ==========================================================
# FUNNEL ANALYSIS
# ==========================================================
#
# Objetivo:
# Analizar cómo avanzan los usuarios a través de las
# diferentes etapas del funnel de la fintech.
#
# Funnel:
#
# sign_up
# ↓
# kyc_completed
# ↓
# first_deposit
# ↓
# card_ordered
# ↓
# first_payment
# ↓
# investment_started
#
# Este análisis permite identificar:
#
# - Cuántos usuarios llegan a cada etapa
# - Dónde se pierde más gente
# - Conversión total hasta inversión
# - Qué planes convierten mejor
#
# ==========================================================


# ----------------------------------------------------------
# Cargar datasets
# ----------------------------------------------------------

df_users = pd.read_csv("data/users.csv")
df_events = pd.read_csv("data/events.csv")

# ----------------------------------------------------------
# Contar eventos
# ----------------------------------------------------------

#Numero de personas que llegan a cada paso 
event_counts = df_events["event"].value_counts()

#Numero total de usuarios registrados
signup = event_counts["sign_up"]

# ----------------------------------------------------------
# Funnel Overview
# ----------------------------------------------------------

print("=== FUNNEL OVERVIEW ===\n")

for event, count in event_counts.items():
    conversion = (count/signup)
    print(
        f"{event}: "
        f"{count} users "
        f"({conversion:.2f}%)"
    )

# ----------------------------------------------------------
# Definir etapas del funnel
# ----------------------------------------------------------

funnel_steps = [
    "sign_up",
    "kyc_completed",
    "first_deposit",
    "card_ordered",
    "first_payment",
    "investment_started"
]

# ----------------------------------------------------------
# Conversión entre pasos consecutivos
# ----------------------------------------------------------

print("\n=== STEP BY STEP CONVERSION ===\n")

dropoffs = {}
#Bucle para recorrer todas las etapas del funnel
for i in range(len(funnel_steps)-1):

    #Etapas
    current_step = funnel_steps[i]
    next_step = funnel_steps[i+1]

    #Numero de personas en cada etapa
    current_count = event_counts[current_step]
    next_count = event_counts[next_step]

    #Tasa de conversion
    conversion = (next_count/current_count)*100

    #Tasa de abandono
    dropoff = 100 - conversion
    dropoffs[f"{current_step} -> {next_step}"] = dropoff

    print(
        f"{current_step} -> {next_step}: "
        f"{conversion:.2f}%"
    )

# ----------------------------------------------------------
# Mayor punto de abandono
# ----------------------------------------------------------
worst_step = max(dropoffs, key=dropoffs.get)

print("\n=== BIGGEST DROPOFF ===\n")
print(
    f"{worst_step}: "
    f"{dropoffs[worst_step]:.2f}% users lost"
)

# ----------------------------------------------------------
# Conversión total del funnel
# ----------------------------------------------------------

#Usuarios que comenzaron a invertir
investment_users = event_counts.get("investment_started", 0)

#Tasa entre paso inicial y final
overall_conversion = (investment_users/signup)*100

print("\n=== OVERALL CONVERSION ===\n")
print(
    f"Signup -> Investment: "
    f"{overall_conversion:.2f}%"
)

# ----------------------------------------------------------
# Conversión a inversión por plan
# ----------------------------------------------------------

#Obetner usuarios que llegaron al paso de invertir
investors = df_events[df_events["event"]=="investment_started"]["user_id"].unique()

#Variable bool si ha invertido o no
df_users["is_investor"] = (df_users["user_id"].isin(investors))

#Tasa de inversión por cada plan
plan_conversion = (df_users.groupby("plan")["is_investor"].mean()*100)

print("\n=== INVESTMENT RATE BY PLAN ===\n")
print(plan_conversion.sort_values(ascending=False))


# ----------------------------------------------------------
# Mejor plan del funnel
# ----------------------------------------------------------

#Mejor plan y su tasa
best_plan  = (plan_conversion.idxmax())
best_rate = (plan_conversion.max())

print("\n=== BEST PLAN ===\n")
print(f"{best_plan}: "f"{best_rate:.2f}%")

# ----------------------------------------------------------
# Funnel por canal de adquisición
# ----------------------------------------------------------

#Tasa de conversion por canal
channel_conversion = (df_users.groupby("acquisition_channel")["is_investor"].mean()*100)

print("\n=== INVESTMENT RATE BY CHANNEL ===\n")
print(channel_conversion.sort_values(ascending=False))

# ----------------------------------------------------------
# Funnel por ocupación
# ----------------------------------------------------------

#Tasa de converison por ocupacion
occupation_conversion = (df_users.groupby("occupation")["is_investor"].mean()*100)

print("\n=== INVESTMENT RATE BY OCCUPATION ===\n")
print(occupation_conversion.sort_values(ascending=False))

# ----------------------------------------------------------
# Mejor segmento de usuarios
# ----------------------------------------------------------

#Tsas de conversion por segmento
segment_conversion = (df_users.groupby(["country", "occupation"])["is_investor"].mean()*100)

#Seleccionar el mejor y su tasa
best_segment = (segment_conversion.idxmax())
best_segment_rate = (segment_conversion.max())

print("\n=== TOP INVESTOR SEGMENT ===\n")
print(
    f"{best_segment[0]} - "
    f"{best_segment[1]} "
    f"({best_segment_rate:.2f}%)"
)

# ----------------------------------------------------------
# Insight automático
# ----------------------------------------------------------

print("\n=== KEY INSIGHTS ===\n")

print(
    f"- The largest user loss occurs at "
    f"{worst_step}."
)

print(
    f"- {best_plan} users show the highest "
    f"investment conversion rate."
)

print(
    f"- {best_segment[0]} "
    f"{best_segment[1]} users are the "
    f"highest converting segment."
)


