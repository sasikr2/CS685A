#!/usr/bin/env python
# coding: utf-8

# # Q3
# 

# In[1]:


import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
import warnings
warnings.filterwarnings("ignore")


# In[2]:


census_raw = pd.read_excel("DDW_PCA0000_2011_Indiastatedist.xlsx")


# In[3]:


data18 = pd.read_excel("DDW-C18-0000.XLSX", skiprows = [0,1,2,4,5])


# In[4]:


data18.head()


# In[5]:


data18_urban = data18[(data18['Urban'] == "Urban") & (data18['Unnamed: 4'] == "Total")]
data18_rural = data18[(data18['Urban'] == "Rural") & (data18['Unnamed: 4'] == "Total")]


# In[6]:


data18_urban.head()


# In[7]:


census = census_raw.iloc[:,6:13]


# In[8]:


census.head()


# In[9]:


census_urban = census[((census["Level"] ==  "STATE") | (census["Level"] == "India")) & (census['TRU'] == "Urban")]
census_urban['Name'] = census_urban['Name'].apply(lambda x: str(x).upper())


# In[10]:


census_urban.head()


# In[11]:


urban_merge = pd.merge(data18_urban, census_urban, how = 'inner', right_on = 'Name', left_on = 'Unnamed: 2')


# In[12]:


urban_merge.head()


# In[13]:


urban_finalt = urban_merge[['Unnamed: 2','Persons','Persons.1', 'TOT_P']]
urban_finalt.rename(columns = {'Unnamed: 2':"states"}, inplace = True)


# In[14]:


urban_finalt.head()


# In[15]:


# urban_final = urban_merge[['Unnamed: 2','TOT_M', "TOT_F",'Males.1',"Females.1"]]
# urban_final.rename(columns = {'Unnamed: 2':"State"}, inplace = True)


# In[16]:


####### Rural ############


# In[17]:


census_rural = census[((census["Level"] ==  "STATE") | (census["Level"] == "India")) & (census['TRU'] == "Rural")]
census_rural['Name'] = census_rural['Name'].apply(lambda x: str(x).upper())


# In[18]:


rural_merge = pd.merge(data18_rural, census_rural, how = 'inner', right_on = 'Name', left_on = 'Unnamed: 2')


# In[19]:


rural_finalt = rural_merge[['Unnamed: 2','Persons','Persons.1', 'TOT_P']]
rural_finalt.rename(columns = {'Unnamed: 2':"states"}, inplace = True)


# In[20]:


# rural_final = rural_merge[['Unnamed: 2','TOT_M', "TOT_F",'Males.1',"Females.1"]]
# rural_final.rename(columns = {'Unnamed: 2':"State"}, inplace = True)


# In[21]:


rural_finalt.head()


# In[22]:


#urban_finalt['urban_perc'] = urban_finalt['Persons.1']/urban_finalt['TOT_P']
#urban_final['urban_perc_female'] =urban_final['Females.1']/urban_final['TOT_P']
#rural_finalt['rural_perc'] =rural_finalt['Persons.1']/rural_finalt['TOT_P']
#rural_final['rural_perc_female'] =rural_final['Females.1']/rural_final['TOT_F']


# In[23]:


urban_finalt.head()


# In[24]:


rural_finalt.head()


# In[25]:


final_si = urban_finalt.copy()
final_si['urban-percentage'] = 100*(urban_finalt['Persons.1']/urban_finalt['TOT_P'])
final_si['rural-percentage'] = 100*(rural_finalt['Persons.1']/rural_finalt['TOT_P'])


# In[26]:


tmp = []
for i in range(final_si.shape[0]):
    succ = np.array([urban_finalt.iloc[i,2],rural_finalt.iloc[i,2]])
    tot_sample = np.array([urban_finalt.iloc[i,3],rural_finalt.iloc[i,3]])
    stats, p_value = proportions_ztest(count = succ, nobs=tot_sample, alternative = 'two-sided')
    tmp.append(p_value)
final_si['p-value'] = np.array(tmp)


# In[27]:


#final_si[['states', 'urban-percentage', 'rural-percentage', 'p-value']]


# In[28]:


final_si[['states', 'urban-percentage', 'rural-percentage', 'p-value']].to_csv("geography-india-c.csv")


# In[29]:


#bilingual


# In[30]:


final_bi = urban_finalt.copy()
final_bi['urban-percentage'] = 100*((urban_finalt['Persons'] - urban_finalt['Persons.1'])/urban_finalt['TOT_P'])
final_bi['rural-percentage'] = 100*((rural_finalt['Persons'] - rural_finalt['Persons.1'])/rural_finalt['TOT_P'])


# In[31]:


tmp = []
for i in range(final_si.shape[0]):
    succ = np.array([urban_finalt.iloc[i,1] - urban_finalt.iloc[i,2],rural_finalt.iloc[i,1] - rural_finalt.iloc[i,2]])
    tot_sample = np.array([urban_finalt.iloc[i,3],rural_finalt.iloc[i,3]])
    stats, p_value = proportions_ztest(count = succ, nobs=tot_sample, alternative = 'two-sided')
    tmp.append(p_value)
final_bi['p-value'] = np.array(tmp)


# In[32]:


final_bi[['states', 'urban-percentage', 'rural-percentage', 'p-value']].to_csv("geography-india-b.csv")


# In[33]:


#final_bi[['states', 'urban-percentage', 'rural-percentage', 'p-value']]


# In[34]:


#lingual


# In[35]:


final_tri = urban_finalt.copy()
final_tri['urban-percentage'] = 100*(1 - ((urban_finalt['Persons'] + urban_finalt['Persons.1'])/urban_finalt['TOT_P']))
final_tri['rural-percentage'] = 100*(1 - ((rural_finalt['Persons'] + rural_finalt['Persons.1'])/rural_finalt['TOT_P']))


# In[36]:


tmp = []
for i in range(final_si.shape[0]):
    succ = np.array([urban_finalt.iloc[i,3]-urban_finalt.iloc[i,1] - urban_finalt.iloc[i,2],rural_finalt.iloc[i,3] -rural_finalt.iloc[i,1] - rural_finalt.iloc[i,2]])
    tot_sample = np.array([urban_finalt.iloc[i,3],rural_finalt.iloc[i,3]])
    stats, p_value = proportions_ztest(count = succ, nobs=tot_sample, alternative = 'two-sided')
    tmp.append(p_value)
final_tri['p-value'] = np.array(tmp)


# In[37]:


final_tri[['states', 'urban-percentage', 'rural-percentage', 'p-value']].to_csv("geography-india-a.csv")


# In[ ]:


print("geography-india-a.csv is created")

print("geography-india-b.csv is created")
print("geography-india-c.csv is created")

# In[ ]:





# In[38]:


# def cal_pvalue(colmt, colms, colft, colfs):
#     pvalue_urban = []
#     for s, s1, a, a1 in zip(colmt, colft, colms, colfs):
#         succ = np.array([a,a1])
#         tot_sample = np.array([s,s1])
#         stats, p_value = proportions_ztest(count = succ, nobs=tot_sample, alternative = 'two-sided')
#         pvalue_urban.append(p_value)
#     return pvalue_urban


# In[40]:


# temp = cal_pvalue(final_data['TOT_M_x'],final_data['Males.1_x'], final_data['TOT_F_x'],final_data['Females.1_x'])
# final_data['urban_pvalue'] = np.array(temp)
# temp = cal_pvalue(final_data['TOT_M_y'],final_data['Males.1_y'], final_data['TOT_F_y'],final_data['Females.1_y'])
# final_data['rural_pvalue'] = np.array(temp)


# In[ ]:


# final_data.head()

