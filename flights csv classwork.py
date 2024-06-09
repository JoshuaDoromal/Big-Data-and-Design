import pandas as pd

flights = pd.read_csv("flights.csv")

#explore data

print(flights.head(4))
print(flights.dtypes)
print(flights["year"].describe())
print(flights["distance"].mean())

#subset
above40 = flights[flights["dep_delay"]>40]

jan_dec = flights[(flights["month"] ==1) | (flights["month"] == 12)]

#filter
JFK_EWR = flights["origin"].isin(["JFK", "EWR"])
carrier_name = flights.loc[flights ["dep_delay"] > 40, "carrier"]

col4 = flights[["carrier", "flight", "origin", "dest"]]

late_arrival = flights[flights["arr_delay"] > 120]

what_happened = flights[(flights["arr_delay"] > 120)& (flights["dep_delay"] <= 0)]

UA_AA_DL = flights[flights['carrier'].isin(["UA", "AA", "DL"])]

summerflights = flights[flights['month'].isin([7, 8, 9])]

tailN111 = flights[flights["tailnum"].str.contains("N111", na=False)]

average_dep_delay_airline = flights.groupby(['carrier'])["dep_delay"].mean().sort_values()

max_airtime_tailnum = flights.groupby(["flight"])["air_time"].max().sort_values()

flights["speed (mph)"] = (flights["distance"] / flights["air_time"] *60)

speeds_of_airlines = (flights["speed (mph)"].sort_values(ascending=False))