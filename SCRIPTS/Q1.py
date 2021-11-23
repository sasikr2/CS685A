#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


data17 = []
for i in range(0,36):
    if i < 10:
        data17.append(pd.read_excel("C-17/DDW-C17-0{}00.XLSX".format(i), skiprows = [0,1,2,4,5]))
    else:
        data17.append(pd.read_excel("C-17/DDW-C17-{}00.XLSX".format(i), skiprows = [0,1,2,4,5]))


# In[5]:


data17[0].head()


# In[6]:


def calc_speakers(data):
    data = data[['Name', "Persons", "Persons.1", "Persons.2"]]
    data = data.dropna(how='all')
    data.fillna(value = 0, inplace = True)
    sum1 = data['Persons'].values.sum()
    sum2 = data['Persons.1'].values.sum()
    si = (sum1-sum2)/sum1*100
    sum3 = data['Persons.2'].values.sum()
    do = (sum2-sum3)/sum1*100
    thi = sum3/sum1*100
    return si, do ,thi


# In[8]:


final_d = {}
final_d['State'] = []
final_d['state-code'] = []
final_d['percent-one'] = []
final_d['percent-two'] = []
final_d['percent-three'] = []
for data in data17:
    a, b, c = calc_speakers(data)
    final_d['State'].append(data["Unnamed: 1"].unique()[0])
    final_d['state-code'].append(data["Code"].unique()[0])
    final_d['percent-one'].append(a)
    final_d['percent-two'].append(b)
    final_d['percent-three'].append(c)


# In[9]:


final_data = pd.DataFrame(final_d)


# In[10]:


final_data.head(40)


# In[15]:


final_data.to_csv("percent-india.csv")
print("percent-india.csv is created")


# In[ ]:




