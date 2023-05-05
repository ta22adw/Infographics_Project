#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 19:06:45 2023

@author: Timothy Atoyebi 22027370
"""

# Assignment 2: Statistics and Trends
# Data source:https://data.worldbank.org/topic/climate-change
#GITHUB : https://github.com/ta22adw/Assignment2
# Import libraries
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


# Load the dataset into a Pandas dataframe
# Import data from the csv file

def read_data(t, a):
    """
    Reads and imports files from comma seperated values, to a python DataFrame

    Arguments:
    a: string, The name of the csv file which is to be read
    b: integer, indicates the number of rows on the csv file to be
    skipped
    
    Returns:
    data: A pandas dataframe with all values from the excel file
    data_t: The transposed pandas dataframe
    """
    data = pd.read_csv(t, skiprows=a)
    data = data.drop(['Country Code', 'Indicator Code'], axis=1)
    t_data = data.set_index(data['Country Name']).T.reset_index().rename(columns={'index': 'Year'})
    t_data = t_data.set_index('Year').dropna(axis=1)
    t_data = t_data.drop(['Country Name'])
    return data, t_data

t = 'WorldbankData.csv'
a = 4

data, t_data = read_data(t, a)
print(t_data)
print(t_data.head)

# Slicing the dataframe to get data for the indicators of interest

def indicator_s(w,x, y, z):
    """
    Reads and selects precise indicators from world bank dataframe, to a python DataFrame

    Arguments:
    w: 'First Indicator'
    x: 'Second Indicator'
    y: 'Third Indicator'
    z: 'Forth Indicator'
    
    Returns:
    ind: A pandas dataframe with all values from 
    """
    ind = data[data['Indicator Name'].isin([w,x, y, z])]
    
    return ind

w = 'Arable land (% of land area)'
x = 'Renewable electricity output (% of total electricity output)'
y = 'Urban population'
z = 'Agricultural land (sq. km)'

i = indicator_s(w,x, y, z)

print(i.head)

# Slicing the dataframe to get data for the countries of interest

def country_s(countries):
    """
    Reads and selects country of interest from world bank dataframe, to a python DataFrame

    Arguments:
    countries: sets of countries selected by me 
    
    Returns:
    selected_c: A pandas dataframe with specific countries selected
    """
    
    selected_c = i[i['Country Name'].isin(countries)]
    selected_c = selected_c.dropna(axis=1)
    selected_c = selected_c.reset_index(drop=True)
    
    return selected_c

# Selecting countries needed

countries = ['United States', 'India', 'China', 'United Kingdom', 'Nigeria', 'South Africa']


selected_c = country_s(countries)
print(selected_c.head)

# STATISTICS OF THE DATA
stats_desc = selected_c.groupby(["Country Name", "Indicator Name"])
print(stats_desc.describe())

def gc_ind(indicator):
    """
    Selects and groups countries based on the specific indicators, to a python DataFrame

    Arguments:
    indicator: 
    
    Returns:
    gc_ind_con: A pandas dataframe with specific countries selected
    """
    gc_ind_con = selected_c[selected_c["Indicator Name"] == indicator]
    gc_ind_con = gc_ind_con.set_index('Country Name', drop=True)
    gc_ind_con = gc_ind_con.transpose().drop('Indicator Name')
    gc_ind_con[countries] = gc_ind_con[countries].apply(pd.to_numeric, errors='coerce', axis=1)
    return gc_ind_con

# Inputting the indicator
Arable_land = gc_ind("Arable land (% of land area)")
print(Arable_land.head())
print(Arable_land.info())

Electricity = gc_ind("Renewable electricity output (% of total electricity output)")
print(Electricity.head())
print(Electricity.info())

Population = gc_ind("Urban population")
print(Population.head())

Agricultural_land = gc_ind("Agricultural land (sq. km)")
print(Agricultural_land.head())

# create line graph
# create for Urban population
plt.figure(figsize=(12, 8))
Population.plot()
plt.title('Urban population')
plt.xlabel('Years')
plt.ylabel('Population In Millions')
plt.rcParams["figure.dpi"] = 300
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# create Electricity Output
plt.figure(figsize=(12, 8))
Electricity.plot()
plt.title('AElectricity Output')
plt.xlabel('Years')
plt.ylabel('sq. km')
plt.rcParams["figure.dpi"] = 300
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# create bar graph 
# create for Electricity Output
plt.figure(figsize=(12, 8))
Electricity.iloc[6:10].plot(kind='bar')
plt.title('Electricity Output')
plt.xlabel('Years')
plt.ylabel('% of total electricity output')
plt.rcParams["figure.dpi"] = 300
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
#Renewable electricity output (% of total electricity output)

# creating Horizontal bar graph 
# create for Urban population
plt.figure(figsize=(12, 8))
Population.iloc[6:10].plot(kind='barh')
plt.title('Urban Population')
plt.xlabel('Years')
plt.ylabel('Population In Millions')
plt.rcParams["figure.dpi"] = 300
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Pie chart
# create Agricultural_land
labels = ['China','United Kingdom','India','Nigeria','United States','South Africa']
countries_a_2010 = Agricultural_land.iloc[20]
plt.figure(figsize=(12,6))
plt.pie(countries_a_2010, labels=labels, autopct='%1.1f%%')
plt.rcParams["figure.dpi"] = 300
plt.title('Agricultural land (sq. km) 2010')
plt.show()

# create for Arable_land
labels = ['South Africa','India','China','United States','Nigeria','United Kingdom']
countries_b_2010 = Arable_land.iloc[20]
plt.figure(figsize=(12,6))
plt.pie(countries_b_2010, labels=labels, autopct='%1.1f%%')
plt.rcParams["figure.dpi"] = 300
plt.title('Arable land (% of land area) 2010')
plt.show()

# Create the dash board

# importing the necessary libraries
import matplotlib.gridspec as gs

plt.style.use('Solarize_Light2')

# creating a figure
fig=plt.figure(figsize=(15, 15), dpi=300)

# creating a gridspec object
gs= gs.GridSpec(ncols=2, nrows=3, figure=fig)

# Creating the First plot (Urban population)
ax1=fig.add_subplot(gs[0, 0]) # line plot
Population.plot(ax=ax1)
ax1.set_title('Urban population', size = 10, fontweight='bold')
ax1.set_xlabel('Years')
ax1.set_ylabel('Population In Millions')

# Creating the Second plot (Agricultural_land)
ax2=fig.add_subplot(gs[0, 1]) # bar plot
Electricity.iloc[6:10].plot(kind='bar', ax=ax2)
ax2.set_title('Electricity Output', size = 10, fontweight='bold')
ax2.set_xlabel('Years')
ax2.set_ylabel('% of total electricity output')

# Creating the Third plot (Agricultural_land)
ax3=fig.add_subplot(gs[1, 0]) # Horizontal bar plot
Population.iloc[6:10].plot(kind='barh', ax=ax3)
ax3.set_title('Urban Population', size = 10, fontweight='bold')
ax3.set_xlabel('Population In Millions')
ax3.set_ylabel('Years')

# Creating the Fourth plot (Electricity Output)
ax4=fig.add_subplot(gs[0, 2]) # bar plot
Electricity.plot(ax=ax4)
ax4.set_title('Electricity Output', size = 10, fontweight='bold')
ax4.set_xlabel('Years')
ax4.set_ylabel('% of total electricity output')

# Creating the Fifth plot (Agricultural_land)
#ax5=fig.add_subplot(gs[1, 1]) # pie chart
#ax5.pie(countries_a_2010, labels=labels,autopct='%.1f%%')
#ax5.set_title('Agricultural land (sq. km) 2010', size = 10, fontweight='bold')

# Save the dashboard as an image
plt.savefig('world_bank_indicators_dashboard.png', bbox_inches='tight', dpi=300)

# Adjust the layout and display the plot
fig.tight_layout()
plt.show()
