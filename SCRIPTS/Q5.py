#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# In[3]:


data13 = []
for i in range(0,36):
    if i < 10:
        data13.append(pd.read_excel("C-13/DDW-0{}00C-13.XLS".format(i), skiprows = [0,1,2,4,5,6]))
    else:
        data13.append(pd.read_excel("C-13/DDW-{}00C-13.XLS".format(i), skiprows = [0,1,2,4,5]))


# In[4]:


datai = data13[0]
datai = datai[datai["Unnamed: 3"] == "India"]
datai = datai[['Unnamed: 3','Unnamed: 4',"Persons"]]


# In[5]:


data13[0].head(100)


# In[6]:


india_age = [1]
stride = [5,5,5,5,5,20,20,31]
temp = datai['Persons'].values
prev = 6
for i in stride:
    india_age.append(temp[prev:prev+i].sum())
    #print(prev, prev+i)
    prev = prev+i
india_age.append(1)
  


# In[7]:


data18 = pd.read_excel("DDW-C18-0000.XLSX", skiprows = [0,1,2,4,5])
# data19 = pd.read_excel("C-19/DDW-C17-0000.XLSX", skiprows = [0,1,2,4])


# In[8]:


data18i = data18[(data18['Unnamed: 2'] == 'INDIA') & (data18['Urban'] == 'Total')]


# In[9]:


data18i['Total_Pop'] = np.array(india_age)


# In[10]:


data18i['Ratio'] = data18i['Persons.1']/data18i['Total_Pop']
data18i.sort_values('Ratio', inplace = True, ascending = False)


# In[11]:


data18i.head(10)


# In[12]:


data18001 = data18i


# In[13]:


districts = data18['Unnamed: 2'].unique()


# In[14]:


data18.head()


# In[15]:


districts


# In[16]:


def make_dist(datai, district, data18):
    #datai = data13[0]\
    #print(datai["Unnamed: 3"].unique())
    #print(datai.shape)
    #print(datai["Unnamed: 3"].unique())
    datai = datai[datai["Unnamed: 3"] == district]
    #print(datai.shape)
    dist_age = [1]
    stride = [5,5,5,5,5,20,20,31]
    temp = datai['Persons'].values
    prev = 6
    for i in stride:
        dist_age.append(temp[prev:prev+i].sum())
        #print(prev, prev+i)
        prev = prev+i
    dist_age.append(1)
    data181i = data18[(data18['Unnamed: 2'] == district) ]
    data181i['Total_Pop'] = np.array(dist_age)  
    data181i['Ratio'] = data181i['Persons.1']/data181i['Total_Pop']
    data181i.sort_values('Ratio', inplace = True, ascending = False)
    return data181i.iloc[2,1], data181i.iloc[2,4]  


# In[17]:


final_dict = {}
final_dict['states'] =[]
final_dict['age_group'] = []
final_dict['percentage'] = []
datat = data13[0]
data13_new = datat[['Unnamed: 3','Unnamed: 4',"Persons"]]
data18_new = data18[(data18['Urban'] == 'Total')]
data18_new = data18_new[['Unnamed: 2','Unnamed: 4','Persons.1']]
data13_new["Unnamed: 3"] = data13_new["Unnamed: 3"].apply(lambda x: str(x).upper() if (str(x) == "India") else str(x)[8:].split(" (")[0])
for district in districts:
    #if district == "INDIA":
    #    continue
    #print(district)
    a, b = make_dist(data13_new,district, data18_new)
    #print(a, b,district)
    final_dict['states'].append(district)
    final_dict['age_group'].append(a)
    final_dict['percentage'].append(b*100)


# In[18]:


final_dict_df = pd.DataFrame(final_dict)


# In[19]:


final_dict_df.head(50)


# In[20]:


final_dict_df.to_csv('age-india.csv')

print("age-india.csv is created")