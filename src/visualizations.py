import pandas as pd
import matplotlib.pyplot as plt

df_events = pd.read_csv("data/events.csv")

#Contar los eventos
event_counts = df_events["event"].value_counts()

#Ordenar funnel
funnel_steps = [
    "sign_up",
    "kyc_completed",
    "first_deposit",
    "card_ordered",
    "first_payment",
    "investment_started"
]

#Crear lista con los valores
counts = []

for step in funnel_steps:
    counts.append(event_counts[step])

#Crear grafico
plt.figure(figsize=(10,5))

plt.bar(
    funnel_steps,
    counts
)

plt.title("User Funnel")

plt.xlabel("Funnel Step")

plt.ylabel("Users")

plt.show()