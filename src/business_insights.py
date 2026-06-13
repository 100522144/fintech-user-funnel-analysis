import pandas as pd 

#Coger los datos del csv

df_users = pd.read_csv("data/users.csv")
df_events = pd.read_csv("data/events.csv")

df_events["timestamp"] = pd.to_datetime(df_events["timestamp"])

#Numero taotal de usuarios

total_users = len(df_users)
print("=== BUSINESS INSIGHTS ===")
print()
print(f"Total Users: {total_users}")

#Tasa de conversión signup deposit
event_counts = df_events["event"].value_counts()

signup = event_counts["sign_up"]
deposit = event_counts["first_deposit"]

deposit_conversion = (deposit/signup)*100

print(f"Signup -> Deposit Conversion: "f"{deposit_conversion:.2f}%")

#Tasa de conversión signup investment

investment = event_counts["investment_started"]

investment_conversion = (investment/signup)*100

print(f"Signup -> Investment Conversion: "f"{investment_conversion:.2f}%")

#Media de los depositos
deposits = df_events[df_events["event"] == "first_deposit"]

average_deposit = deposits["deposit_amount"].mean()

print(f"Average Deposit Amount: "f"€{average_deposit:.2f}")


#Mejor canal de adquisición
investors = df_events[df_events["event"] == "investment_started"][["user_id"]]
investors["is_investor"] = True

df = pd.merge(df_users, investors, on="user_id", how="left")

df["is_investor"] = df["is_investor"].fillna(False)

channel_conversion = (df.groupby("acquisition_channel")["is_investor"].mean()*100)

best_channel = channel_conversion.idxmax()
best_channel_rate = channel_conversion.max()

print()
print("Best Acquisition Channel:")
print(
    f"{best_channel} "
    f"({best_channel_rate:.2f}%)"
)

#Que plan depsoita dinero más rápido
signup = df_events[df_events["event"] == "sign_up"][["user_id","timestamp"]]


deposit = df_events[df_events["event"] == "first_deposit"][["user_id","timestamp"]]

signup = signup.rename(columns={"timestamp":"signup_date"})

deposit = deposit.rename(columns={"timestamp":"deposit_date"})

time_df = pd.merge(signup,deposit,on="user_id")

time_df["days_to_deposit"] = (time_df["deposit_date"]-time_df["signup_date"]).dt.days


time_df = pd.merge(time_df,df_users[["user_id","plan"]],on="user_id")

plan_speed = time_df.groupby("plan")["days_to_deposit"].mean()

fastest_plan = plan_speed.idxmin()

fastest_days = plan_speed.min()

print()
print("Fastest Converting Plan:")
print(
    f"{fastest_plan} "
    f"({fastest_days:.2f} days)"
)