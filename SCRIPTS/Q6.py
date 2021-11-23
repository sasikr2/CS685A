#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# In[2]:
data8 = pd.read_excel("DDW-0000C-08.xlsx", skiprows = [0,1,2,3,5,6])

# In[3]:

data8.head()

# In[4]:
datai = data8[(data8['Unnamed: 5'] == 'All ages') & (data8['Unnamed: 4'] == 'Total')]


# In[5]:


datai.head()


# In[6]:


datai["Unnamed: 3"] = datai["Unnamed: 3"].apply(lambda x: str(x).upper() if (str(x) == "INDIA") else str(x)[8:])


# In[7]:


data19 = pd.read_excel("DDW-C19-0000.xlsx",skiprows = [0,1,2,4,5])


# In[8]:


datae = data19[data19['Urban/'] == 'Total']
datae = datae[["Unnamed: 2","Unnamed: 4" ,"Persons.1", "Males.1","Females.1"]]


# In[9]:


datae.head()


# In[10]:


districts = datae['Unnamed: 2'].unique()


# In[11]:


# Illiterate   ==> 1
# Literate   ==> 2
# Literate but below primary   ==> 4
# Primary but below middle    ==> 5
# Middle but below matric/secondary   ==> 6
# Matric/Secondary but below graduate   ==> 7
# Graduate and above        ==> 11


# In[13]:


def make_dist(datai, district, data19i):
    # datai = data13[0]\
    # print(datai["Unnamed: 3"].unique())
    datai = datai[datai["Unnamed: 3"] == district]
    #print(datai.shape, data19.shape)
    mx = 0
    st = 0
    for i in range(0,7):
        tot = datai.iloc[0,i+1]
        succ  = data19i.iloc[i+1,2]
        #grp.append(data19.iloc[i+1,1])
        if (succ / tot) > mx:
            mx = (succ / tot)
            st = i
#         tott.append(tot)
#         succs.append(succ)
        if(mx > 1.0):
            pass
            #print(datai)
            #print(data19i)
    return mx*100,data19i.iloc[st+1,1]

final_dict = {}
final_dict['states'] =[]
final_dict['literacy-group'] = []
final_dict['percentage'] = []
datai_new = datai[['Unnamed: 3','Persons.1','Persons.2','Persons.4','Persons.5','Persons.6','Persons.7','Persons.11',]]
for district in districts:
    #if district == "INDIA":
    #    continue
#     print(district)
    dataee = datae[datae['Unnamed: 2'] == district]
    a, b = make_dist(datai_new,district, dataee)
#     print(a, b,district)
    final_dict['states'].append(district)
    final_dict['literacy-group'].append(b)
    final_dict['percentage'].append(a)

# districts

final_dict_df = pd.DataFrame(final_dict)

final_dict_df.to_csv('literacy-india.csv')

print("literacy-india.csv is created")

