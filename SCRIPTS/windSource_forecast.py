#!/usr/bin/env python
# coding: utf-8

# In[20]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.stattools import adfuller, acf, pacf
from scipy.optimize import curve_fit
import  statsmodels.api as sm
import itertools
import warnings 
warnings.filterwarnings("ignore")


# In[21]:


df = pd.read_csv("Electricity Generation by Source_D_20211110_093557.csv", skiprows = [0], header = 1,parse_dates = ["YearValue"], index_col = 'YearValue')


# In[22]:


df


# In[23]:


df.sort_values('YearValue', inplace = True)


# In[24]:


df['EnergySource'].unique()


# In[25]:


dfcoal  = df[df['EnergySource']  == "WIND"]
dfcoal =dfcoal[['Generation_GWh']]
dfcoalshift = dfcoal - dfcoal.shift()
dfcoalshift.dropna(inplace = True)


# In[26]:


from pylab import rcParams
rcParams['figure.figsize'] = (18, 8)
decomposition = sm.tsa.seasonal_decompose(dfcoal['Generation_GWh'], model='additive')
fig = decomposition.plot()
plt.show()


# In[27]:


p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 2) for x in list(itertools.product(p, d, q))]


# In[28]:


param1 = ()
param2 = ()
mxaic = 1000000000
for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(dfcoal['Generation_GWh'],
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            results = mod.fit()
            if(mxaic > results.aic):
                mxaic = results.aic
                param1 = param
                param2 = param_seasonal
            #print('ARIMA{}x{}2 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue


# In[29]:


#ARIMA(1, 1, 1)x(1, 0, 1, 2)12 - AIC:27.277687091576425
print(param1, param2)


# In[30]:


mod = sm.tsa.statespace.SARIMAX(dfcoal['Generation_GWh'],
                                order=param1,
                                seasonal_order=param2,
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])


# In[ ]:





# In[31]:


pred = results.get_prediction(start=pd.to_datetime('2006-01-01'), dynamic=False)
pred_ci = pred.conf_int()
ax = dfcoal['2006':].plot()
pred.predicted_mean.plot(ax = ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
# ax.fill_between(pred_ci.index,
#                 pred_ci.iloc[:, 0],
#                 pred_ci.iloc[:, 1], color='k', alpha=.2)
ax.set_xlabel('Years')
ax.set_ylabel('Ratio of non-renewable and renewable')
plt.legend()
plt.show()


# In[39]:


y_forecasted = np.array(pred.predicted_mean)
y_truth = np.array(dfcoal['2006':])
#print(y_forecasted,y_truth)
mse = ((y_forecasted[1:] - y_truth[1:])**2).mean()
print('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse)/1000, 2)))


# In[40]:


pred_uc = results.get_forecast(steps=10)
pred_ci = pred_uc.conf_int()

ax = dfcoal.plot(label='observed', figsize=(14, 7))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                 pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Year')
ax.set_ylabel('Ratio')
plt.legend()
plt.show()


# In[41]:


df_pred = pd.DataFrame(pred_uc.predicted_mean)


# In[42]:


df_pred


# In[44]:


final = pd.concat([dfcoal, df_pred])
final.to_csv("wind_source_forecast.csv")


# In[ ]:




