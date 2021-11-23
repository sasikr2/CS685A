#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import ensemble


# In[2]:


# df = pd.read_csv(StringIO("anomaly-s058.dat"), engine='python')
df = pd.read_csv("anomaly-s058.dat", sep="\t", header  = None)


# In[3]:


df  = df.dropna(axis = 1)


# In[4]:


df.head()


# In[5]:


df.describe()


# In[6]:


x = df.to_numpy()


# In[7]:


xwhole = x.reshape((x.shape[0]*x.shape[1], 1))


# In[8]:


print(xwhole.mean(), xwhole.std())
print(x.mean(), x.std())


# In[9]:


xtrain = xwhole.copy()
model  =  ensemble.IsolationForest(n_estimators=200,contamination=.021,bootstrap=True, n_jobs=-1, random_state=20, verbose=0, warm_start=False)
model.fit(xtrain)
a_s = model.decision_function(xtrain)
pred = model.predict(xtrain)


# In[10]:


print(a_s)


# In[11]:


print(np.sum(pred == -1), np.sum(pred == 1))


# In[12]:


mas = np.array((pred == -1))*1
print(mas.shape)


# In[13]:


mas = mas.reshape((mas.shape[0],1))


# In[14]:


_ = plt.figure(figsize = (10,6))
plt.plot(xwhole,'o')
plt.plot(xwhole*mas, 'ro')


# In[15]:


xans1 = mas.reshape((100, 100))


# In[16]:


# file = open(filename, "r")
file = open("answer-s058.dat","w")
for i in range(100):
    for j in range(100):
        file.write(str(xans1[i][j]))
        if(j != 99):
            file.write("\t")
    file.write("\n")
file.close()


# In[17]:


df2 = pd.read_csv("answer-s058.dat", sep="\t", header  = None)


# In[18]:


print("answer-s058.dat is created")

