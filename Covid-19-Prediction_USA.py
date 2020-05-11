

import numpy as np
import pandas as pd
import warnings
from fbprophet import Prophet
warnings.simplefilter('ignore')

url = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'

#Load Data
countries_aggregated_data = pd.read_csv(url, error_bad_lines=False)

#Check if there is anull values
countries_aggregated_data.isnull().sum()

US_Confirmed_Cases=countries_aggregated_data.loc[countries_aggregated_data['Country'] == 'US', ('Date','Confirmed')]

#replace index value to start with 0
US_Confirmed_Cases.index = range(0,len(US_Confirmed_Cases))

#Plot
fig = US_Confirmed_Cases.set_index('Date')['Confirmed'].plot()


confirmed = US_Confirmed_Cases.copy()
confirmed.columns = ['ds','y']

#Covert to datetime
confirmed['ds'] = pd.to_datetime(confirmed['ds'])


confirmed.head()


#Drop zero Values
confirmed.drop(confirmed[confirmed.y ==0 ].index, inplace=True)

length =int (confirmed.shape[0]*0.80)
#Split to Train set and test set
train_set=confirmed.iloc[:length]
test_set=confirmed.iloc[length:]


model=Prophet(interval_width=0.95,
               weekly_seasonality=False,
              daily_seasonality=False,
              yearly_seasonality=False)
model.add_seasonality('daily', period=1, fourier_order=5)
model.add_seasonality('weekly', period=7, fourier_order=35)
model.add_seasonality('Monthly', period=30.5, fourier_order=20)

model.fit(train_set)
#predict 20 days
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

#plot
confirmed_forecast_plot = model.plot(forecast)

forecast_components = model.plot_components(forecast)

#Prepare
test_forecast = forecast[forecast.index >= length]

test_score = test_forecast.set_index('ds')[['yhat']].join(test_set.set_index('ds').y).reset_index()


#Drop zero Values
test_score.dropna(inplace=True)

from sklearn.metrics import mean_squared_error, mean_absolute_error
print('MAE:', mean_absolute_error(test_score.yhat, test_score.y))
print('RMSE:',np.sqrt(mean_squared_error(test_score.yhat, test_score.y)))



