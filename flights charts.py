# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 10:45:12 2024

@author: joshd
"""

import pandas as pd

#import the dataset flights.csv
flights = pd.read_csv("flights.csv")

flights.dtypes

#piecahrt
viz1 = flights['origin'].value_counts()

#create vizi pie chart
viz1.plot.pie()

#create vizq pie chart
viz2 = flights['carrier'].value_counts()

#create vizi bar chart
viz2.plot.bar()

#count flights per month
viz3 = flights['month'].value_counts()

# sort flights col 0
viz3 = viz3.sort_index(axis = 0)

viz3.plot.line()

# find all the dealys per hour on 05-3-2013
viz4 = flights["dep_delay"].value_counts()

# subset of boxplot
viz5 = flights [(flights["day"]==5) & (flights["month"]==3)]

#boxplot
viz5.plot.box(column=['dep_delay'], by="hour")

#scatter plot










