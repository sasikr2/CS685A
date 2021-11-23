#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest


# In[6]:


data17 = []
for i in range(0,36):
    if i < 10:
        data17.append(pd.read_excel("C-17/DDW-C17-0{}00.XLSX".format(i), skiprows = [0,1,2,4,5]))
    else:
        data17.append(pd.read_excel("C-17/DDW-C17-{}00.XLSX".format(i), skiprows = [0,1,2,4,5]))


# In[7]:


d = data17[0]
d.head()


# In[2]:


#c19 ==> eduacation level and speaking lang
#c18 ==>    age group and lang


# In[8]:


def calc_speakers(data):
    data = data[['Name', "Males", "Males.1", "Males.2", 'Females',  'Females.1',  'Females.2']]
    data = data.dropna(how='all')
    data.fillna(value = 0, inplace = True)
    sum1 = data['Males'].values.sum()
    sum2 = data['Males.1'].values.sum()
    si = (sum1-sum2)#/sum1*100
    sum3 = data['Males.2'].values.sum()
    do = (sum2-sum3)#/sum1*100
    thi = sum3#/sum1*100
    sum11 = data['Females'].values.sum()
    sum21 = data['Females.1'].values.sum()
    sif = (sum11-sum21)#/sum11*100
    sum31 = data['Females.2'].values.sum()
    dof = (sum21-sum31)#/sum11*100
    thif = sum31#/sum11*100
    return sum1, si, do ,thi, sum11, sif, dof, thif


# In[9]:


final_d1 = {}
final_d2 = {}
final_d3 = {}
final_d1['state-code'] = []
final_d2['state-code'] = []
final_d3['state-code'] = []
final_d1['state'] = []
final_d2['state'] = []
final_d3['state'] = []

#final_d['Total Male'] = []
#final_d['Total Female'] = []
#final_d['Male One lang Speaker'] = []
#final_d['Female One lang Speaker'] = []
#final_d['Male Two lang Speaker'] = []
#final_d['Female Two lang Speaker'] = []
#final_d['Male Three lang Speaker'] = []
#final_d['Female Three lang Speaker'] = []
final_d1['male-percentage'] = []
final_d1['female-percentage'] = []
final_d2['male-percentage'] = []
final_d2['female-percentage'] = []
final_d3['male-percentage'] = []
final_d3['female-percentage'] = []
final_d1['p-value'] = []
final_d2['p-value'] = []
final_d3['p-value'] = []

for data in data17:
    s, a, b, c, s1, a1, b1, c1 = calc_speakers(data)
    final_d1['state'].append(data["Unnamed: 1"].unique()[0])
    final_d2['state'].append(data["Unnamed: 1"].unique()[0])
    final_d3['state'].append(data["Unnamed: 1"].unique()[0])
    final_d1['state-code'].append(data["Code"].unique()[0])
    final_d2['state-code'].append(data["Code"].unique()[0])
    final_d3['state-code'].append(data["Code"].unique()[0])
    
#     final_d['Total Male'].append(s)
#     final_d['Total Female'].append(s1)
#     final_d['Male One lang Speaker'].append(a)
#     final_d['Male Two lang Speaker'].append(b)
#     final_d['Male Three lang Speaker'].append(c)
#     final_d['Female One lang Speaker'].append(a1)
#     final_d['Female Two lang Speaker'].append(b1)
#     final_d['Female Three lang Speaker'].append(c1)
    final_d1['male-percentage'].append(a/s*100)
    final_d1['female-percentage'].append(a1/s1*100)
    final_d2['male-percentage'].append(b/s*100)
    final_d2['female-percentage'].append(b1/s1*100)
    final_d3['male-percentage'].append(c/s*100)
    final_d3['female-percentage'].append(c1/s1*100)
    succ = np.array([a,a1])
    tot_sample = np.array([s,s1])
    stats, p_value = proportions_ztest(count = succ, nobs=tot_sample, alternative = 'two-sided')
    final_d1['p-value'].append(p_value)
    if(p_value >= 0.025):
        print(data["Unnamed: 1"].unique()[0])
    succ = np.array([b,b1])
    stats, p_value = proportions_ztest(count = succ, nobs=tot_sample, alternative = 'two-sided')
    final_d2['p-value'].append(p_value)
    if(p_value >= 0.025):
        print("2",data["Unnamed: 1"].unique()[0])
    succ = np.array([c,c1])
    stats, p_value = proportions_ztest(count = succ, nobs=tot_sample, alternative = 'two-sided')
    final_d3['p-value'].append(p_value)
    
    sum1 = a1+b1+c1
    if(sum1 < 99.9):
        print(data["Unnamed: 1"].unique()[0])


# In[10]:


final_data1 = pd.DataFrame(final_d1)
final_data2 = pd.DataFrame(final_d2)
final_data3 = pd.DataFrame(final_d3)


# In[13]:


final_data3.head(36)


# In[98]:


final_data1.to_csv("gender-india-a.csv")
final_data2.to_csv("gender-india-b.csv")
final_data3.to_csv("gender-india-c.csv")
print("gender-india-a.csv is created")
print("gender-india-b.csv is created")
print("gender-india-c.csv is created")

