# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 11:40:22 2024

@author: joshd
"""

import pandas as pd
import streamlit as st
import plotly_express

df = pd.read_csv("flights.csv")
df = df.iloc[1:1000]

#title
st.title["Flights Dashboard"]
st.text["A data story of all the flights from 3 main airports in New York in 2013"]

#sidebar
st.sidebar.header("sidebar here")

origin = st.sidebar.multiselect(
    "select origin"
    options=df["origin"].unique()
    default=df["origin"].unique()
    )

carrier = st.sidebar.multiselect(
    "select carrier"
    options=df["carrier"].unique()
    default=df["carrier"].unique()
    )


#fillter with a query
df_selection = df.query(
    "origin == @origin & carrier == @carrier"
    )

if st.checkbox ("Show raw data"):
   st.subheader("raw data")
   st.dataframe(df)
   
#add basic stats
   
total_delay = int(df_selection["dep_delay"].sum())
averave_delay = round(df_selection ["dep_delay"].mean(),1)

st.markdown("""___""")

#columns for basic stats
left_column, middle_column, right_column = st._column(3)

with left_column:
    st.subheader("total dealy:")
    st.subheader(f"")
            






