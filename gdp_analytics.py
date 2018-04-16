import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display
import seaborn

#load US stocks and GDP datasets
stocks = pd.read_csv('stocks.csv')
gdp = pd.read_csv('gdp.csv')

#set year as the index for stocks data frame
stocks = stocks.set_index(['Year'])

#rename the columns and set year as the index for gdp data frame
gdp = gdp.rename(columns={'Unnamed: 0':'Year', 'GDP in billions of chained 2009 dollars':'Real GDP in billions'})
gdp = gdp.set_index(['Year'])
gdp.head()

#drop the nomial gdp column
gdp = gdp.drop('GDP in billions of current dollars', axis = 1)
gdp.head()

#merge gdp and stocks to one data frame and drop rows that contains Na
newData = pd.concat([gdp, stocks], axis = 1)
newData = newData.dropna()

#create a new column called GDP growth rate
newData.loc[1929, 'Real GDP in billions']
newData['GDP copy'] = newData['Real GDP in billions']

#create a function to calculate GDP growth rate
def growth ():
    n = 1930
    for n in range(1930, 2015):
        newData['GDP copy'].ix[n] = newData['Real GDP in billions'].ix[n-1]
        n += 1
    newData['GDP Growth Rate'] = (newData['Real GDP in billions']-newData['GDP copy'])/ newData['GDP copy']

#call the function, perform the calculation
growth()

#drop all unneeded columns
newData = newData.drop(['Stocks','T.Bills','T.Bonds','GDP copy', 'Stocks - Bills', 'Stocks - Bonds'], axis=1)
newData.head()

#format rate of returns and GDP growth rate to percent
newData['S&P 500'] = pd.Series(['{0:.2f}%'.format(val*100) for val in newData['S&P 500']],
                                    index = newData.index)
newData['3-month T.Bill'] = pd.Series(['{0:.2f}%'.format(val*100) for val in newData['3-month T.Bill']],
                                    index = newData.index)
newData['10-year T. Bond'] = pd.Series(['{0:.2f}%'.format(val*100) for val in newData['10-year T. Bond']],
                                    index = newData.index)
newData['GDP Growth Rate']= pd.Series(['{0:.2f}%'.format(val*100) for val in newData['GDP Growth Rate']],
                                    index = newData.index)

#find the top5 years with highest GDP growth rate
newData['GDP Growth Rate'].sort_values(ascending = False).head()

#find the top 5 years with highest rate of return for S&P 500 stocks
newData['S&P 500'].sort_values(ascending = False).head()

#find the top 5 years with highest rate of return for T.Bill
newData['3-month T.Bill'].sort_values(ascending = False).head()

#find the top 5 years with highest rate of return for T. bond
newData['10-year T. Bond'].sort_values(ascending = False).head()

#create function to plot real GDP for selected year range

def gdp_range(y1, y2):
    data = newData.loc[y1:y2,'Real GDP in billions']
    plot = data.plot(kind = 'line', title =str(y1)+' - '+ str(y2)+ ' US GDP', figsize = (10, 5), fontsize=12)
    plt.xlabel('Year')
    plt.ylabel('$ in billions')
    
    #create function to format y label and make it display with commas
    def update_labels(ax):
        ylabels = [format(label, ',.0f') for label in ax.get_yticks()]
        ax.set_yticklabels(ylabels)
    update_labels(plot)
    
    plt.show()

#plot real GDP from 2000 to 2015
gdp_range(2000, 2015)

#create function to plot all 3 types of stocks rate of return for selected year range 

def plotRR(y1, y2):
    newData['S&P 500'] = newData['S&P 500'].replace('%', '', regex=True).astype('float')
    newData['3-month T.Bill'] = newData['3-month T.Bill'].replace('%', '', regex=True).astype('float')
    newData['10-year T. Bond'] = newData['10-year T. Bond'].replace('%', '', regex=True).astype('float')
    data = newData.loc[y1:y2, 'S&P 500':'10-year T. Bond']
    plot = data.plot(kind = 'line', title =str(y1)+' - '+ str(y2)+ ' US Stock Rate of Returns',figsize =(15, 6),fontsize=12)
    plt.xlabel('Year')
    plt.ylabel('Rate of Return %')   
    plt.show()

plotRR(2000,2015)

#create function to plot GDP growth rate and rate of return of T.Bills in one plot

def gdp_Tbill(y1, y2):
    data = newData.loc[y1:y2]
    data1 = data.loc[:,'3-month T.Bill']
    plot = data1.plot(kind='line', label='T.Bill Rate of Return')
    data.loc[:,'GDP Growth Rate'].plot(kind = 'line' ,ax = plot, figsize=(10,5), fontsize=12)
    plt.legend(loc='best')
    plt.title(str(y1)+' - '+str(y1)+' US GDP Growth Rate vs. T.Bill Rate of Return')
    plt.xlabel('Year')
    plt.ylabel('%')
    plt.show()

gdp_Tbill(2000,2015)

#create function to plot GDP growth rate and stocks rate of return in one plot

def gdp_Tbond(y1, y2):
    data = newData.loc[y1:y2]
    data1 = data.loc[:,'10-year T. Bond']
    plot = data1.plot(kind='line', label='T. Bond Rate of Return')
    data.loc[:,'GDP Growth Rate'].plot(kind = 'line' ,ax = plot, figsize=(10,5), fontsize=12)
    plt.legend(loc='best')
    plt.title(str(y1)+' - '+str(y1)+' US GDP Growth Rate vs. T.Bond Rate of Return')
    plt.xlabel('Year')
    plt.ylabel('%')
    plt.show()

gdp_Tbond(2000,2015)