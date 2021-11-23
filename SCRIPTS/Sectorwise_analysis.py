#!/usr/bin/env python
# coding: utf-8

# In[129]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


# In[130]:


df = pd.read_csv("Electricity Consumption by Consuming Sector_D_20211110_094023.csv", skiprows = [0], header= 1)


# In[131]:


sector  = df['ConsumingSector'].unique()


# In[132]:


df.head()


# In[133]:


sectorb = df['BroadCategory'].unique()


# In[135]:


year = df['YearValue'].unique()


# In[137]:


df_l4 = df[((df['YearValue'] >= 2012) & (df['YearValue'] <= 2019))]


# In[138]:


data_sectorwise = []
for se in sector:
    data_sectorwise.append(df_l4[(df_l4['ConsumingSector'] == se) ])


# In[139]:


# fig = plt.figure()
# plt.plot(df_l4_s31['YearValue'].values ,df_l4_s31['Consumption_GWh'].values, '-',  label = sector[0],)
# # plt.scatter(x = np.arange(df_l4_s32.shape[0]), y = df_l4_s32['Consumption_GWh'].values, label = sector[1])
# # plt.scatter(x = np.arange(df_l4_s33.shape[0]), y = df_l4_s33['Consumption_GWh'].values, label = sector[2])
# # plt.scatter(x = np.arange(df_l4_s34.shape[0]), y = df_l4_s34['Consumption_GWh'].values, label = sector[3])
# plt.legend()


# In[146]:


fig = plt.figure(figsize = (15,10))
ax = plt.subplot(111)
for i in range(8):
    ax.plot(data_sectorwise[i]['YearValue'].values ,data_sectorwise[i]['Consumption_GWh'].values, '-',  label = sector[i])
    
plt.xlabel("Years", fontsize = 13)
plt.ylabel("Generation(GHw)", fontsize = 13)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


# In[101]:


# fig = 
# px.bar(df_l4_s31, x="YearValue", y=["Consumption_GWh" ], barmode='group', height = 400 )
# px.bar(df_l4_s32, x="YearValue", y=["Consumption_GWh" ], barmode='group', height = 400)
# fig.show()


# In[102]:



fig = plt.figure()
x = np.arange(8)

plt.bar(x - 0.1, df_l4_s31['Consumption_GWh'], width = 0.2)
plt.bar(x+0.1, df_l4_s32['Consumption_GWh'], width = 0.2)


# In[ ]:




