#!/usr/bin/env python
# coding: utf-8

# In[123]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from imblearn.over_sampling import SMOTE
from sklearn.metrics import confusion_matrix
import sys


# In[2]:


df = pd.read_csv("training-s058.csv", header= None)


# In[3]:


df = df.sort_values(0)


# In[4]:


num_class = df.iloc[:,0].nunique()
class_label = df.iloc[:,0].unique()
print(class_label, num_class)


# In[5]:


for c in class_label:
    x = df[df[0] == c]
    print(c, x.shape)


# In[6]:


df['label'], _ = df[0].factorize()


# In[7]:


df = df.sample(frac=1)


# In[8]:


df_y  = df['label']
df_x = df.iloc[:,1:-1]


# In[9]:


df_x.describe()


# In[11]:


xtrain = df_x.to_numpy()
ytrain = df_y.to_numpy()


# In[12]:


ytrain = ytrain.reshape((ytrain.shape[0], 1))


# In[13]:


print(xtrain.shape, ytrain.shape)


# In[117]:


xmean = xtrain.mean(axis = 0)
xstd = xtrain.std(axis = 0)


# In[118]:


print(xmean, xstd)


# In[16]:


xtrainm = (xtrain - xmean[np.newaxis, :])/xstd[np.newaxis, :]


# In[17]:


print(xtrainm.mean(axis = 0), xtrainm.std(axis = 0))


# In[18]:


print(ytrain[0:5], xtrain[0:5])


# In[19]:


sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_resample(xtrainm, ytrain)


# In[20]:


print(X_res.shape )


# In[61]:


from sklearn.ensemble import RandomForestClassifier
modelr = RandomForestClassifier(max_depth=3, random_state=0)
results = modelr.fit(X_res, y_res)


# In[ ]:





# In[105]:


class mycallbacks(tf.keras.callbacks.Callback):
        def on_epoch_end(self,epoch,logs = {}):
            if(logs.get('accuracy') > 0.990):
                print("\nReached 98% accuracy so cancelling training!")
                self.model.stop_training = True


# In[106]:


model = tf.keras.models.Sequential([tf.keras.layers.Dense(128,activation = tf.nn.relu),
                                    tf.keras.layers.Dropout(.2),
                                    tf.keras.layers.Dense(64,activation = tf.nn.relu), 
                                    tf.keras.layers.Dense(num_class, activation = tf.nn.softmax)])


# In[107]:


opt = tf.keras.optimizers.RMSprop(
    learning_rate=0.001)
opt1 = tf.keras.optimizers.Adam(
    learning_rate=0.001)


# In[108]:


model.compile(optimizer=opt1,
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])


# In[109]:


callbacks = mycallbacks()
history = model.fit(X_res, y_res, epochs = 80, batch_size= 32,callbacks = [callbacks])


# In[110]:


acc=history.history['accuracy']
# val_acc=history.history['val_acc']
loss=history.history['loss']
# val_loss=history.history['val_loss']

epochs=range(len(acc)) # Get number of epochs

#------------------------------------------------
# Plot training and validation accuracy per epoch
#------------------------------------------------
# plt.plot(epochs, acc, 'r', "Training Accuracy")
_ = plt.figure()
plt.plot(epochs, loss, 'r', "Training loss")
# plt.plot(epochs, val_acc, 'b', "Validation Accuracy")
plt.title('Training loss')
_ = plt.figure()
plt.plot(epochs, acc, 'r', "Training Accuracy")


# In[111]:


pred = model.predict(xtrainm[0:])
pred1 = pred.argmax(axis = 1)


# In[112]:


p = 0
p1 = 0
n = 0
tpt  = 0
for i in range(pred1.shape[0]):
    tot = i
    x = pred1[i]
    if(x == ytrain[i]):
        p = p +1
    else:
#         print(x, ytrain[i])
        n = n+1
        
        


# In[113]:


print(p/tot, n/tot,p,n, tot)


# In[114]:


confusion_matrix(ytrain, pred1)


# In[48]:


class_map = {}
i = 0
for cl in class_label:
    class_map[i] = cl
    i = i+1


# In[124]:


test_filename = sys.argv[1]
print("testfilename = {}".format(test_filename))


# In[51]:


test = pd.read_csv(test_filename, header = None)
xtest = test.iloc[:,1:].to_numpy()
xtest_norm = (xtest - xtest.mean(axis = 0)[np.newaxis,:])/xtest.std(axis = 0)[np.newaxis,:]
ypred = model.predict(xtest_norm)
ypredl = ypred.argmax(axis = 1)
res = []
for yp in ypredl:
    res.append(class_map[yp])
# test.iloc[:,0] = np.array(res)


# In[120]:


final  = pd.Series(res)


# In[125]:


try:
    final.to_csv("classifier-s058.csv")
    print("classifier-s058.csv is created")
except:
    print("error in creation of classifier-s058.csv")


# In[ ]:




