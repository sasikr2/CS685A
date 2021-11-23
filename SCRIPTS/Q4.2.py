#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[3]:


data17 = []
for i in range(0,36):
    if i < 10:
        data17.append(pd.read_excel("C-17/DDW-C17-0{}00.XLSX".format(i), skiprows = [0,1,2,4,5]))
    else:
        data17.append(pd.read_excel("C-17/DDW-C17-{}00.XLSX".format(i), skiprows = [0,1,2,4,5]))


# In[4]:


# data18 = pd.read_excel("C-18/DDW-C17-0000.XLSX", skiprows = [0,1,2,4])
# data19 = pd.read_excel("C-19/DDW-C17-0000.XLSX", skiprows = [0,1,2,4])


# In[5]:


#c19 ==> eduacation level and speaking lang
#c18 ==>    age group and lang


# In[6]:


def calc_speakers(data):
    data = data[['Name', "Persons", "Persons.1", "Persons.2"]]
    data = data.dropna(how='all')
    data.fillna(value = 0, inplace = True)
    sum1 = data['Persons'].values.sum()
    sum2 = data['Persons.1'].values.sum()
    si = (sum1-sum2)#/sum1*100
    sum3 = data['Persons.2'].values.sum()
    do = (sum2-sum3)#/sum1*100
    thi = sum3#/sum1*100
    return si, do ,thi


# In[40]:


final_d = {}
final_d['State'] = []
final_d['One lang Speaker'] = []
final_d['Two lang Speaker'] = []
final_d['Three lang Speaker'] = []
final_d['Ratio_3to2'] = []
final_d['Ratio_2to1'] = []
for data in data17:
    a, b, c = calc_speakers(data)
    final_d['State'].append(data["Unnamed: 1"].unique()[0])
    final_d['One lang Speaker'].append(a)
    final_d['Two lang Speaker'].append(b)
    final_d['Three lang Speaker'].append(c)
    final_d['Ratio_3to2'].append(c/b)
    final_d['Ratio_2to1'].append(b/a)


# In[41]:


final_data = pd.DataFrame(final_d)


# In[42]:


final_data.head(40)


# In[53]:


final_data = final_data.sort_values("Ratio_3to2", ascending = False)


# In[54]:


top_data = final_data.iloc[0:3,:]
below_data = final_data.iloc[-3:,:]
below_data = below_data.sort_values("Ratio_3to2")


# In[55]:


top_data.head()


# In[56]:


final32 = pd.concat([top_data, below_data])


# In[57]:


final32.head(7)


# In[48]:


final_data = final_data.sort_values("Ratio_2to1", ascending = False)
top_data = final_data.iloc[0:3,:]
below_data = final_data.iloc[-3:,:]
below_data = below_data.sort_values("Ratio_2to1")
final21 = pd.concat([top_data, below_data])


# In[49]:


final21.head()


# In[60]:


#final32[['State','Ratio_3to2']].to_csv("3-to-2-ratio.csv")
final21[['State','Ratio_2to1']].to_csv("2-to-1-ratio.csv")
print("2-to-1-ratio.csv is created")


# In[ ]:




