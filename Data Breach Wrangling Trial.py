# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 00:54:26 2024

@author: joshd
"""

import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns


df = pd.read_csv("Data Breaches.csv")

#Control df
df_2 = pd.read_csv("Data Breaches.csv")


#what does the df look like
df.shape

#what types of info is inside
df.dtypes

#Drop the column 'Sources' since it's not useful
df.drop(['Sources'], axis=1, inplace=True)

#finding which column has null data
df.isnull().any()

#merging the years together that are anomalies
df['Year'] = df['Year'].astype(str)
df['Year'] = df['Year'].str[:4]
df['Year'] = df['Year'].astype(int)

# Convert 'Year' column to datetime
df['Year'] = pd.to_datetime(df['Year'], format='%Y').dt.to_period('Y')

# finding more info about the column 'Year'
table_year_df = df['Year'].value_counts()

#checking the change
df.dtypes

#visualize it as a bar chart, in order of count
table_year_df.plot.bar(xlabel='Year')
plt.title('Amount of Data Breaches')
plt.xlabel('Years')
plt.ylabel('Amount of Breaches')

#arrange the df with the oldest year first
table_year_df_2 = table_year_df.sort_index(ascending=True)

#visualize it as a bar chart, in order of year
table_year_df_2.plot.bar(xlabel='Year')
plt.title('Amount of Data Breaches')
plt.xlabel('Years')
plt.ylabel('Amount of Breaches')


#visualize it as a line chart, in order of year
table_year_df_2.plot.line(x='Years')
plt.title('Amount of Data Breaches')
plt.xlabel('Years')
plt.ylabel('Amount of Breaches')

#sorting the different types of breach methods
table1 = df['Method'].value_counts()
table1_1 = table1.head(10)

#vis table1_1
table1_1.plot.bar()
plt.title('Data Breaches by Method')
plt.xlabel('Method')
plt.ylabel('Amount of Breaches')


#listing out the Org types
table2 = df['Organization type'].value_counts()
table2_2 = table2.head(15)


#vis table2_2
table2_2.plot.bar()
plt.title('Data Breaches by Organization Type')
plt.xlabel('Organization Type')
plt.ylabel('Amount of Breaches')

# Convert 'Records' to numeric, errors='coerce' will set non-convertible values to NaN, then dropna to remove them
df['Records'] = pd.to_numeric(df['Records'], errors='coerce')
df.dropna(subset=['Records'], inplace=True)

# Reset index after dropping rows
df.reset_index(drop=True, inplace=True)

# Grouping everything by year and summing records
df_records_per_year = df.groupby('Year', as_index=False)["Records"].sum()

# Plotting table3
table3 = df_records_per_year.plot.line(x='Year', y='Records', xlabel='Year', ylabel='Total Records')
plt.title('Amount of Records Breached per Year')


# Finding repeat entities and their details
repeat_entities_details = df[df['Entity'].isin(df[df.duplicated('Entity')]['Entity'])]
repeat_entities_summary = repeat_entities_details.groupby('Entity').agg(
    Times_Repeated=('Entity', 'size'),
    Years=('Year', lambda x: list(x)),
    Total_Records_Lost=('Records', 'sum')
).reset_index()

repeat_entities_summary

#  Bar plot for Times_Repeated for each Entity
plt.figure(figsize=(10, 6))
sns.barplot(x='Times_Repeated', y='Entity', data=repeat_entities_summary.sort_values('Times_Repeated', ascending=False))
plt.title('Number of Times Each Entity is Repeated')
plt.xlabel('Times Repeated')
plt.ylabel('Entity')
plt.show()


