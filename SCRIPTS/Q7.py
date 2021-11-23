#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[40]:


data17 = []
map1 = {}
for i in range(0,36):
    if i < 10:
        data17.append(pd.read_excel("C-17/DDW-C17-0{}00.XLSX".format(i), skiprows = [0,1,2,4,5], usecols = range(5)))
        map1[data17[i]["Unnamed: 1"].unique()[0]] = i
    else:
        data17.append(pd.read_excel("C-17/DDW-C17-{}00.XLSX".format(i), skiprows = [0,1,2,4,5], usecols = range(5)))
        map1[data17[i]["Unnamed: 1"].unique()[0]] = i


# In[ ]:


# North: JK, $Ladakh$, PN, HP, HR, UK, Delhi, Chandigar   8
# West: RJ, GJ, MH, Goa, Dadra & Nagar Haveli, Daman & Diu 6
# Central: MP, UP, CG 3
# East: BH, WB, OR, JH  4
# South: KT, $TG$, AP, TN, KL, Lakshadweep, Puducherry   7
# North-East: AS, SK, MG, TR, AR, MN, NG, MZ, Andaman & Nicobar     9


# In[10]:


dict1 = {"North": [
 'JAMMU & KASHMIR','PUNJAB','HIMACHAL PRADESH','HARYANA','UTTARAKHAND','NCT OF DELHI', 'CHANDIGARH'],
         "West": ['RAJASTHAN', 'GUJARAT', 'DADRA & NAGAR HAVELI','MAHARASHTRA',"GOA", 'DAMAN & DIU'],
         'Central': ["MADHYA PRADESH", "UTTAR PRADESH", "CHHATTISGARH"],
         "East": ["BIHAR", "JHARKHAND","ODISHA", "WEST BENGAL"],
         "South": ['ANDHRA PRADESH', 'KARNATAKA','LAKSHADWEEP','KERALA','TAMIL NADU','PUDUCHERRY'],
         "North-East": ['NAGALAND','MANIPUR', 'MIZORAM', 'TRIPURA', 'MEGHALAYA','ASSAM', 'ANDAMAN & NICOBAR ISLANDS', "SIKKIM",'ARUNACHAL PRADESH']
        }

l = [('HINDI','PUNJABI','ENGLISH'),('HINDI','MARATHI','GUJARATI'),
     ('HINDI','ENGLISH','URDU'),('HINDI','BENGALI','ODIA'),('TELUGU','TAMIL','KANNADA'),('ASSAMESE','BENGALI','HINDI') ]

# In[45]:


datas = []
for key in dict1:
    l = dict1[key]
    data = pd.DataFrame()
    for dist in l:
        idx = map1[dist]
        #print(idx)
        d = data17[idx].dropna()
        #print(d.shape)
        data = pd.concat([data, d])    
    datas.append(data)    


# In[89]:


final_dict = {}
final_dict["Region"] = []
final_dict['Language-1'] = []
final_dict['Language-2'] = []
final_dict['Language-3'] = []
i = 0
for reg in dict1:
    final_dict['Region'].append(reg)
    x = datas[i].groupby("Name").sum().sort_values(by = 'Persons', ascending = False)
    final_dict['Language-1'].append(x.index[0])
    final_dict['Language-2'].append(x.index[1])
    final_dict['Language-3'].append(x.index[2])
    i += 1




# In[90]:


final_data = pd.DataFrame(final_dict)


# In[91]:


final_data.head()

final_dict1 = {}
final_dict1["Region"] = []
final_dict1['Language-1'] = []
final_dict1['Language-2'] = []
final_dict1['Language-3'] = []
i = 0
l = [('HINDI','PUNJABI','ENGLISH'),('HINDI','MARATHI','GUJARATI'),
     ('HINDI','ENGLISH','URDU'),('HINDI','BENGALI','ODIA'),('TELUGU','TAMIL','KANNADA'),('ASSAMESE','BENGALI','HINDI') ]
for reg in dict1:
    final_dict1['Region'].append(reg)
    x = datas[i].groupby("Name").sum().sort_values(by = 'Persons', ascending = False)
    a, b , c = l[i]
    print(a,b,c)
    final_dict1['Language-1'].append(x.index[0])
    final_dict1['Language-2'].append(b)
    final_dict1['Language-3'].append(c)
    i += 1
# In[92]:
final_data1 = pd.DataFrame(final_dict1)
final_data1.to_csv("region-india-b.csv")

final_data.to_csv("region-india-a.csv")


# In[ ]:


print("region-india-a.csv is created")
print("region-india-b.csv is created")

