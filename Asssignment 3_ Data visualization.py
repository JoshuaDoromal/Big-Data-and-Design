# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 23:54:37 2024

@author: joshd
"""

import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('movie_plots-1.csv')

# Group the data by origin/ethnicity and count the number of rows (movies) in each group
movies_per_origin = df.groupby('Origin/Ethnicity').size()

# Print the result (you can also save it to a new DataFrame or use it for further analysis)
print(movies_per_origin)

# Group the data by origin/ethnicity and release year, then count the number of movies for each group
grouped_data = df.groupby(['Origin/Ethnicity', 'Release Year']).size().reset_index(name='Number of Movies')

# Create a line chart for each origin/ethnicity
unique_origins = grouped_data['Origin/Ethnicity'].unique()
for origin in unique_origins:
    data_subset = grouped_data[grouped_data['Origin/Ethnicity'] == origin]
    plt.plot(data_subset['Release Year'], data_subset['Number of Movies'], label=origin)

# Customize the plot
plt.xlabel('Release Year')
plt.ylabel('Number of Movies')
plt.title('Movies Produced by Origin/Ethnicity Over Time')
# Adjust the legend to a more rectangular shape and position it below the plot to avoid covering the x-axis title
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), shadow=True, ncol=4)

#------------------------------------------------------------------------------------------------------------------------------

# Load the dataset
df = pd.read_csv('flights.csv')

# Define a function to categorize flight duration
def categorize_flight(hour):
    if hour < 6:
        return 'Short Haul'
    elif 6 <= hour <= 16:
        return 'Long Haul'
    else:
        return 'Ultra Long Haul'

# Apply the function to create a new column for flight category
df['Flight Category'] = df['hour'].apply(categorize_flight)

# Group the data by carrier and flight category, then count the number of flights in each category
grouped_data = df.groupby(['carrier', 'Flight Category']).size().unstack(fill_value=0)

# Plotting
fig, ax = plt.subplots(figsize=(10, 8))

# Create a clustered column chart
grouped_data.plot(kind='bar', ax=ax, width=0.8)

# Customizing the plot
ax.set_xlabel('Carrier', fontsize=14)
ax.set_ylabel('Quantity of Flights', fontsize=14)
ax.set_title('Flight Duration Categories by Carrier', fontsize=16)
ax.legend(title='Flight Category')

plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()    
    
    
    
