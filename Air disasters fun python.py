#import pandas
import pandas as pd

# reading csv
df = pd.read_excel("airdisaster.xlsx")

df_drop_NA = df.dropna()

df_time = df_drop_NA.drop(columns=["time"])

df_new = df["crew"].str.split("/", expand = True)

df["Fatalities-crew"] = df_new[0]
df["Fatalities-occupants"] = df_new[1]

df=df.drop(columns=['crew'])

df["Fatalities-crew"] = df["Fatalities-crew"].str.replace("Fatalities:", "")
df["Fatalities-occupants"] = df["Fatalities-occupants"].str.replace("Occupants:", "")

df.info()

df["Fatalities-crew"] = pd.to_numeric(df["Fatalities-crew"], errors = 'coerce')

df.info()

