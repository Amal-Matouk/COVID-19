


import pandas as pd
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go

#Load
Data = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv')

#
Data.head()


#Check null values

Data.isnull().sum()

#Check Types
Data.dtypes

#Change Types
Data["Date"]=Data["Date"].astype('datetime64[ns]')


Data.dtypes

# Total Confirmed arround the world
#World_Data Data Frame
World_Data = pd.DataFrame()

#Calculate Confirmed ,Deaths, Recoverd cases
sums=Data.sum(axis = 0, skipna = True ,numeric_only = True).to_frame()
World_Data =sums.T

#Calculate Active cases
World_Data["Active"] = World_Data["Confirmed"] - World_Data["Deaths"] - World_Data["Recovered"]

#Print
World_Data

#plot pie
fig = px.pie(World_Data,
                        values = World_Data.iloc[0],
                        names= World_Data.columns.values,
                        color_discrete_sequence=px.colors.sequential.RdBu,
                        title='Total Cases')
fig.show()

#plot Map
#Define Color scale
Color_Scale = ["#eafcfd","#b7e0e4","#85c5d3","#60a7c7","#4989bc","#3e6ab0","#3d4b94","#323268","#1d1d3b","#030512"]
fig = px.choropleth(Confirmed_Cases_Per_Country,
                    locations=Confirmed_Cases_Per_Country['Country'],
                    color=Confirmed_Cases_Per_Country['Confirmed'],
                    locationmode='country names',
                    hover_name=Confirmed_Cases_Per_Country['Country'],
                    color_continuous_scale=Color_Scale)
fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        title='Confirmed Cases In The World',
)
fig.show()


# Confirmed Cases Per Country sotred desc
Confirmed_Cases_Per_Country = Data.groupby(["Country"])["Confirmed"].sum().reset_index().sort_values("Confirmed",ascending=False)

# Print
Confirmed_Cases_Per_Country.head()

# Plot Confirmed_Cases_Per_Country bar
fig = px.bar(Confirmed_Cases_Per_Country[0:20],
             x = 'Country',
             y = 'Confirmed',
             color='Country',
             title='Top(20) Countries - Confirmed')
fig.show()

# Deaths Cases Per Country sotred desc
Death_Cases_Per_Country = Data.groupby(["Country"])["Deaths"].sum().reset_index().sort_values("Deaths",ascending=False)

# Print
Death_Cases_Per_Country.head()

# Plot Death_Cases_Per_Country bar
fig = px.bar(Death_Cases_Per_Country[0:20],
             x = 'Country',
             y = 'Deaths',
             color='Country',
             title='Top(20) Countries - Deaths')
fig.show()


# Recovered Cases Per Country sotred desc
Recovered_Cases_Per_Country = Data.groupby(["Country"])["Recovered"].sum().reset_index().sort_values("Recovered",ascending=False)

# Print
Recovered_Cases_Per_Country.head()

# Plot Recovered_Cases_Per_Country bar
fig = px.bar(Recovered_Cases_Per_Country[0:20],
             x = 'Country',
             y = 'Recovered',
             color='Country',
             title='Top(20) Countries - Recovered')
fig.show()


Info_Table = pd.DataFrame()

Info_Table =pd.merge(pd.merge(Confirmed_Cases_Per_Country,Death_Cases_Per_Country,on='Country'),Recovered_Cases_Per_Country,on='Country')


Info_Table["Active"] = Info_Table["Confirmed"]-Info_Table["Deaths"]-Info_Table["Recovered"]
Info_Table["Deaths/Confirmed"]=Info_Table["Deaths"]/Info_Table["Confirmed"]

Info_Table["Confirmed/Total"]=Info_Table.Confirmed/World_Data.iloc[0]["Confirmed"]
Info_Table["Deaths/Total"]=Info_Table["Deaths"]/World_Data.iloc[0]["Deaths"]


Info_Table.head()


#Plot Info Table

Table_Fig = go.Figure(data=[go.Table(
                 columnwidth = [80,80],
    header=dict(values=list(Info_Table.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[Info_Table['Country'],
                       Info_Table['Confirmed'],
                       Info_Table['Deaths'],
                       Info_Table['Recovered'],
                       Info_Table['Active'],
                       round(Info_Table['Deaths/Confirmed'],3),
                       round(Info_Table['Confirmed/Total'],3),
                       round(Info_Table['Deaths/Total'],3)
                       ],
               fill_color='lavender',
               align='left'))
])

Table_Fig.show()

# Total Cases Per Date
Total_Cases_Per_Date  = Data.groupby(["Date"])[["Confirmed","Deaths","Recovered"]].sum().reset_index()

#Plot Confirmed Per Date
fig = px.line(Total_Cases_Per_Date, x="Date", y="Confirmed", title='Confirmed Per Date')
plot(fig)
