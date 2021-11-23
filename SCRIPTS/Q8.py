#!/usr/bin/env python
# coding: utf-8

# In[89]:


import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# In[90]:


#a = pd.read_excel("C-17/DDW-C17-0{}00.XLSX".format(0), skiprows = [0,1,2,4,5])
#a.head()


# In[91]:


data13 = []
for i in range(0,36):
    if i < 10:
        data13.append(pd.read_excel("C-13/DDW-0{}00C-13.XLS".format(i), skiprows = [0,1,2,4,5,6]))
    else:
        data13.append(pd.read_excel("C-13/DDW-{}00C-13.XLS".format(i), skiprows = [0,1,2,4,5]))


# In[92]:


data18 = pd.read_excel("DDW-C18-0000.XLSX", skiprows = [0,1,2,4,5])
# data19 = pd.read_excel("C-19/DDW-C17-0000.XLSX", skiprows = [0,1,2,4])


# In[93]:


districts = data18['Unnamed: 2'].unique()


# In[94]:


data18.head()


# In[95]:


districts


# In[96]:


def make_dist(datai, district, data18, category = "Persons"):
    #datai = data13[0]
    #print(datai["Unnamed: 3"].unique())
    #print(datai.shape)
    #print(datai["Unnamed: 3"].unique())
    datai = datai[datai["Unnamed: 3"] == district]
    #print(datai.shape)
    dist_age = [1]
    stride = [5,5,5,5,5,20,20,31]
    temp = datai[category].values
    prev = 6
    for i in stride:
        dist_age.append(temp[prev:prev+i].sum())
        #print(prev, prev+i)
        prev = prev+i
    dist_age.append(1)
    data181i = data18[(data18['Unnamed: 2'] == district) ]
    data181i['Total_Pop'] = np.array(dist_age)  
    data181i['Ratio'] = data181i[category+'.1']/data181i['Total_Pop']
    data181i.sort_values('Ratio', inplace = True, ascending = False)
    return data181i.iloc[2,1], data181i.iloc[2,4]
    


# In[97]:


final_dict = {}
final_dict['states'] =[]
final_dict['age-group-males'] = []
final_dict['ratio-males'] = []
datat = data13[0]
data13_new = datat[['Unnamed: 3','Unnamed: 4',"Males"]]
data18_new = data18[(data18['Urban'] == 'Total')]
data18_new = data18_new[['Unnamed: 2','Unnamed: 4','Males.1']]
data13_new["Unnamed: 3"] = data13_new["Unnamed: 3"].apply(lambda x: str(x).upper() if (str(x) == "India") else str(x)[8:].split(" (")[0])
for district in districts:
    #if district == "INDIA":
    #    continue
    #print(district)
    a, b = make_dist(data13_new,district, data18_new, "Males")
    #print(a, b,district)
    final_dict['states'].append(district)
    final_dict['age-group-males'].append(a)
    final_dict['ratio-males'].append(b)


# In[98]:


final_dict_dfm2 = pd.DataFrame(final_dict)
final_dict_dfm2.head(50)


# In[99]:


#females
final_dict = {}
final_dict['states'] =[]
final_dict['age-group-females'] = []
final_dict['ratio-females'] = []
datat = data13[0]
data13_new = datat[['Unnamed: 3','Unnamed: 4',"Females"]]
data18_new = data18[(data18['Urban'] == 'Total')]
data18_new = data18_new[['Unnamed: 2','Unnamed: 4','Females.1']]
data13_new["Unnamed: 3"] = data13_new["Unnamed: 3"].apply(lambda x: str(x).upper() if (str(x) == "India") else str(x)[8:].split(" (")[0])
for district in districts:
    #if district == "INDIA":
    #    continue
    #print(district)
    a, b = make_dist(data13_new,district, data18_new, "Females")
    #print(a, b,district)
    final_dict['states'].append(district)
    final_dict['age-group-females'].append(a)
    final_dict['ratio-females'].append(b)


# In[100]:


final_dict_dff2 = pd.DataFrame(final_dict)
final_dict_dff2.head(50)


# In[101]:


final_data = pd.merge(final_dict_dfm2, final_dict_dff2, how = 'outer', right_on = 'states', left_on = 'states')


# In[102]:


final_data.to_csv("age-gender-a.csv")
print("age-gender-a.csv is created")



# In[103]:


#c19 ==> eduacation level and speaking lang
#c18 ==>    age group and lang


# In[104]:


#bi


# In[105]:


def make_dist_bilingual(datai, district, data18, category = "Persons"):
    #datai = data13[0]\
    #print(datai["Unnamed: 3"].unique())
    
    #print(datai.shape)
    #print(datai["Unnamed: 3"].unique())
    datai = datai[datai["Unnamed: 3"] == district]
    #print(datai.shape)
    dist_age = [1]
    stride = [5,5,5,5,5,20,20,31]
    temp = datai[category].values
    prev = 6
    for i in stride:
        dist_age.append(temp[prev:prev+i].sum())
        #print(prev, prev+i)
        prev = prev+i
    dist_age.append(1)
    data181i = data18[(data18['Unnamed: 2'] == district) ]
    data181i['Total_Pop'] = np.array(dist_age)  
    data181i['Ratio'] = (data181i[category] - data181i[category+'.1'])/data181i['Total_Pop']
    data181i.sort_values('Ratio', inplace = True, ascending = False)
    #print(data181i.columns)
    return data181i.iloc[2,1], data181i.iloc[2,5]
    


# In[106]:


final_dict = {}
final_dict['states'] =[]
final_dict['age-group-males'] = []
final_dict['ratio-males'] = []
datat = data13[0]
data13_new = datat[['Unnamed: 3','Unnamed: 4',"Males"]]    # total population
data18_new = data18[(data18['Urban'] == 'Total')]
data18_new = data18_new[['Unnamed: 2','Unnamed: 4','Males.1', 'Males']]

data13_new["Unnamed: 3"] = data13_new["Unnamed: 3"].apply(lambda x: str(x).upper() if (str(x) == "India") else str(x)[8:].split(" (")[0])
for district in districts:
    #if district == "INDIA":
    #    continue
    #print(district)
    a, b = make_dist_bilingual(data13_new,district, data18_new, "Males")
    #print(a, b,district)
    final_dict['states'].append(district)
    final_dict['age-group-males'].append(a)
    final_dict['ratio-males'].append(b)


# In[107]:


final_dict_dfm1 = pd.DataFrame(final_dict)
final_dict_dfm1.head()


# In[108]:


final_dict = {}
final_dict['states'] =[]
final_dict['age-group-females'] = []
final_dict['ratio-females'] = []
datat = data13[0]
data13_new = datat[['Unnamed: 3','Unnamed: 4',"Females"]]    # total population
data18_new = data18[(data18['Urban'] == 'Total')]
data18_new = data18_new[['Unnamed: 2','Unnamed: 4','Females.1', 'Females']]

data13_new["Unnamed: 3"] = data13_new["Unnamed: 3"].apply(lambda x: str(x).upper() if (str(x) == "India") else str(x)[8:].split(" (")[0])
for district in districts:
    #if district == "INDIA":
    #    continue
    #print(district)
    a, b = make_dist_bilingual(data13_new,district, data18_new, "Females")
    #print(a, b,district)
    final_dict['states'].append(district)
    final_dict['age-group-females'].append(a)
    final_dict['ratio-females'].append(b)


# In[ ]:


final_dict_dff1 = pd.DataFrame(final_dict)
final_dict_dff1.head()


# In[ ]:


final_data_bi = pd.merge(final_dict_dfm1, final_dict_dff1, how = 'outer', right_on = 'states', left_on = 'states')
final_data_bi.to_csv("age-gender-b.csv")
print("age-gender-b.csv is created")



# In[ ]:


def make_dist_lingual(datai, district, data18, category = "Persons"):
    #datai = data13[0]\
    #print(datai["Unnamed: 3"].unique())
    
    #print(datai.shape)
    #print(datai["Unnamed: 3"].unique())
    datai = datai[datai["Unnamed: 3"] == district]
    #print(datai.shape)
    dist_age = [1]
    stride = [5,5,5,5,5,20,20,31]
    temp = datai[category].values
    prev = 6
    for i in stride:
        dist_age.append(temp[prev:prev+i].sum())
        #print(prev, prev+i)
        prev = prev+i
    dist_age.append(1)
    data181i = data18[(data18['Unnamed: 2'] == district) ]
    data181i['Total_Pop'] = np.array(dist_age)  
    data181i['Ratio'] = 1 - ((data181i[category] +data181i[category+'.1'])/data181i['Total_Pop'])
    data181i.sort_values('Ratio', inplace = True, ascending = False)
    #print(data181i.columns)
    return data181i.iloc[2,1], data181i.iloc[2,5]
    


# In[ ]:


final_dict = {}
final_dict['states'] =[]
final_dict['age-group-males'] = []
final_dict['ratio-males'] = []
datat = data13[0]
data13_new = datat[['Unnamed: 3','Unnamed: 4',"Males"]]    # total population
data18_new = data18[(data18['Urban'] == 'Total')]
data18_new = data18_new[['Unnamed: 2','Unnamed: 4','Males.1', 'Males']]

data13_new["Unnamed: 3"] = data13_new["Unnamed: 3"].apply(lambda x: str(x).upper() if (str(x) == "India") else str(x)[8:].split(" (")[0])
for district in districts:
    #if district == "INDIA":
    #    continue
    #print(district)
    a, b = make_dist_lingual(data13_new,district, data18_new, "Males")
    #print(a, b,district)
    final_dict['states'].append(district)
    final_dict['age-group-males'].append(a)
    final_dict['ratio-males'].append(b)


# In[ ]:


final_dict_dfm = pd.DataFrame(final_dict)
final_dict_dfm.head()


# In[ ]:


final_dict = {}
final_dict['states'] =[]
final_dict['age-group-females'] = []
final_dict['ratio-females'] = []
datat = data13[0]
data13_new = datat[['Unnamed: 3','Unnamed: 4',"Females"]]    # total population
data18_new = data18[(data18['Urban'] == 'Total')]
data18_new = data18_new[['Unnamed: 2','Unnamed: 4','Females.1', 'Females']]

data13_new["Unnamed: 3"] = data13_new["Unnamed: 3"].apply(lambda x: str(x).upper() if (str(x) == "India") else str(x)[8:].split(" (")[0])
for district in districts:
    #if district == "INDIA":
    #    continue
    #print(district)
    a, b = make_dist_lingual(data13_new,district, data18_new, "Females")
    #print(a, b,district)
    final_dict['states'].append(district)
    final_dict['age-group-females'].append(a)
    final_dict['ratio-females'].append(b)


# In[ ]:


final_dict_dff = pd.DataFrame(final_dict)
final_dict_dff.head()


# In[ ]:


final_data_si = pd.merge(final_dict_dfm, final_dict_dff, how = 'outer', right_on = 'states', left_on = 'states')


# In[ ]:


final_data_si.to_csv("age-gender-c.csv")
print("age-gender-c.csv is created")
