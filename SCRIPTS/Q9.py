#!/usr/bin/env python
# coding: utf-8

# In[104]:


import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")


data8 = pd.read_excel("DDW-0000C-08.xlsx", skiprows = [0,1,2,3,5,6])


# In[106]:


data19 = pd.read_excel("DDW-C19-0000.xlsx",skiprows = [0,1,2,4,5])


# In[107]:


data19e = data19[data19['Urban/'] == 'Total']
data19e = data19e[["Unnamed: 2","Unnamed: 4" ,"Persons", "Males", "Females","Persons.1", "Males.1","Females.1"]]


# In[108]:


data8.head()


# In[109]:


data8i = data8[(data8['Unnamed: 5'] == 'All ages') & (data8['Unnamed: 4'] == 'Total')]


# In[110]:


data8i.head()


# In[111]:


data8i["Unnamed: 3"] = data8i["Unnamed: 3"].apply(lambda x: str(x).upper() if (str(x) == "INDIA") else str(x)[8:])


# In[112]:


data19e.head(10)


# In[113]:


districts = data19e['Unnamed: 2'].unique()


# In[114]:


# Illiterate   ==> 1
# Literate   ==> 2
# Literate but below primary   ==> 4
# Primary but below middle    ==> 5
# Middle but below matric/secondary   ==> 6
# Matric/Secondary but below graduate   ==> 7
# Graduate and above        ==> 11


# In[115]:


def make_dist(datai, district, data19i, idx):
    # datai = data13[0]\
    #print(datai["Unnamed: 3"].unique())
    datai = datai[datai["Unnamed: 3"] == district]
    #print(datai.shape, data19.shape)
    mx = 0
    st = 0
    for i in range(0,7):
        tot = datai.iloc[0,i+1]
        succ  = data19i.iloc[i+1,idx]   #data19
        #print(succ)
        #grp.append(data19.iloc[i+1,1])
        if (succ / tot) > mx:
            mx = (succ / tot)
            st = i
#         tott.append(tot)
#         succs.append(succ)
        if(mx > 1.0):
            #print(datai)
            #print(data19i)
            pass
    return mx,data19i.iloc[st+1,1]

    


# In[116]:


final_dict = {}
final_dict['states'] =[]
final_dict['literacy-group-males'] = []
final_dict['ratio-males'] = []
category = 'Males'
datai_new = data8i[['Unnamed: 3',category+'.1',category+'.2',category+'.4',category+'.5',category+'.6',category+'.7',category+'.11',]]
for district in districts:
    #if district == "INDIA":
    #    continue
#     print(district)
    data19ee = data19e[data19e['Unnamed: 2'] == district]
    a, b = make_dist(datai_new,district, data19ee, 6)
#     print(a, b,district)
    final_dict['states'].append(district)
    final_dict['literacy-group-males'].append(b)
    final_dict['ratio-males'].append(a)


# In[117]:


final_dict_dfm3 = pd.DataFrame(final_dict)
final_dict_dfm3.head(50)


# In[118]:


final_dict = {}
final_dict['states'] =[]
final_dict['literacy-group-females'] = []
final_dict['ratio-females'] = []
category = 'Females'
datai_new = data8i[['Unnamed: 3',category+'.1',category+'.2',category+'.4',category+'.5',category+'.6',category+'.7',category+'.11',]]
for district in districts:
    #if district == "INDIA":
    #    continue
#     print(district)
    data19ee = data19e[data19e['Unnamed: 2'] == district]
    a, b = make_dist(datai_new,district, data19ee, 7)
#     print(a, b,district)
    final_dict['states'].append(district)
    final_dict['literacy-group-females'].append(b)
    final_dict['ratio-females'].append(a)


# In[119]:


final_dict_dff3 = pd.DataFrame(final_dict)
final_dict_dff3.head(50)


# In[120]:


final_data_tri = pd.merge(final_dict_dfm3, final_dict_dff3, how = 'outer', right_on = 'states', left_on = 'states')


# In[121]:


final_data_tri.to_csv('literacy-gender-a.csv')
print("literacy-gender-a.csv is created")


# In[122]:


def make_dist_bilingual(datai, district, data19i, idx):
    # datai = data13[0]\
    #print(datai["Unnamed: 3"].unique())
    datai = datai[datai["Unnamed: 3"] == district]
    #print(datai.shape, data19.shape)
    mx = 0
    st = 0
    for i in range(0,7):
        tot = datai.iloc[0,i+1]
        succ  = data19i.iloc[i+1,idx] - data19i.iloc[i+1, idx+2]   #data19
        #print(succ)
        #grp.append(data19.iloc[i+1,1])
        if (succ / tot) > mx:
            mx = (succ / tot)
            st = i
#         tott.append(tot)
#         succs.append(succ)
        if(mx > 1.0):
            #print(datai)
            #print(data19i)
            pass
    return mx,data19i.iloc[st+1,1]


# In[123]:


final_dict = {}
final_dict['states'] =[]
final_dict['literacy-group-males'] = []
final_dict['ratio-males'] = []
category = 'Males'
datai_new = data8i[['Unnamed: 3',category+'.1',category+'.2',category+'.4',category+'.5',category+'.6',category+'.7',category+'.11',]]
for district in districts:
    #if district == "INDIA":
    #    continue
#     print(district)
    data19ee = data19e[data19e['Unnamed: 2'] == district]
    a, b = make_dist_bilingual(datai_new,district, data19ee, 4)
#     print(a, b,district)
    final_dict['states'].append(district)
    final_dict['literacy-group-males'].append(b)
    final_dict['ratio-males'].append(a)


# In[124]:


final_dict_dfm2 = pd.DataFrame(final_dict)
final_dict_dfm2.head(50)


# In[125]:


final_dict = {}
final_dict['states'] =[]
final_dict['literacy-group-females'] = []
final_dict['ratio-females'] = []
category = 'Females'
datai_new = data8i[['Unnamed: 3',category+'.1',category+'.2',category+'.4',category+'.5',category+'.6',category+'.7',category+'.11',]]
for district in districts:
    #if district == "INDIA":
    #    continue
#     print(district)
    data19ee = data19e[data19e['Unnamed: 2'] == district]
    a, b = make_dist(datai_new,district, data19ee, 5)
#     print(a, b,district)
    final_dict['states'].append(district)
    final_dict['literacy-group-females'].append(b)
    final_dict['ratio-females'].append(a)


# In[126]:


final_dict_dff2 = pd.DataFrame(final_dict)
final_dict_dff2.head(50)


# In[127]:


final_data_bi = pd.merge(final_dict_dfm2, final_dict_dff2, how = 'outer', right_on = 'states', left_on = 'states')


# In[128]:


final_data_bi.to_csv('literacy-gender-b.csv')
print("literacy-gender-b.csv is created")


# In[129]:


def make_dist_single(datai, district, data19i, idx):
    # datai = data13[0]\
    #print(datai["Unnamed: 3"].unique())
    datai = datai[datai["Unnamed: 3"] == district]
    #print(datai.shape, data19.shape)
    mx = 0
    st = 0
    for i in range(0,7):
        tot = datai.iloc[0,i+1]
        succ  = data19i.iloc[i+1,idx] + data19i.iloc[i+1,idx+2]   #data19
        #print(succ)
        #grp.append(data19.iloc[i+1,1])
        if (1 - (succ / tot)) > mx:
            mx = (1 - (succ / tot))
            st = i
#         tott.append(tot)
#         succs.append(succ)
        if(mx > 1.0):
            #print(datai)
            #print(data19i)
            pass
    return mx,data19i.iloc[st+1,1]


# In[130]:


final_dict = {}
final_dict['states'] =[]
final_dict['literacy-group-males'] = []
final_dict['ratio-males'] = []
category = 'Males'
datai_new = data8i[['Unnamed: 3',category+'.1',category+'.2',category+'.4',category+'.5',category+'.6',category+'.7',category+'.11',]]
for district in districts:
    #if district == "INDIA":
    #    continue
#     print(district)
    data19ee = data19e[data19e['Unnamed: 2'] == district]
    a, b = make_dist_single(datai_new,district, data19ee, 4)
#     print(a, b,district)
    final_dict['states'].append(district)
    final_dict['literacy-group-males'].append(b)
    final_dict['ratio-males'].append(a)


# In[131]:


final_dict_dfm1 = pd.DataFrame(final_dict)
final_dict_dfm1.head(50)


# In[132]:


final_dict = {}
final_dict['states'] =[]
final_dict['literacy-group-females'] = []
final_dict['ratio-females'] = []
category = 'Females'
datai_new = data8i[['Unnamed: 3',category+'.1',category+'.2',category+'.4',category+'.5',category+'.6',category+'.7',category+'.11',]]
for district in districts:
    #if district == "INDIA":
    #    continue
#     print(district)
    data19ee = data19e[data19e['Unnamed: 2'] == district]
    a, b = make_dist_single(datai_new,district, data19ee, 5)
#     print(a, b,district)
    final_dict['states'].append(district)
    final_dict['literacy-group-females'].append(b)
    final_dict['ratio-females'].append(a)


# In[133]:


final_dict_dff1 = pd.DataFrame(final_dict)
final_dict_dff1.head(50)


# In[134]:


final_data_si = pd.merge(final_dict_dfm1, final_dict_dff1, how = 'outer', right_on = 'states', left_on = 'states')


# In[135]:


final_data_si.to_csv('literacy-gender-c.csv')
print("literacy-gender-c.csv is created")

