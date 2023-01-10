#!/usr/bin/env python
# coding: utf-8

# In[79]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, roc_auc_score, roc_curve, f1_score


# In[80]:


data = pd.read_csv("C:/Users/33789/OneDrive/Desktop/Project 3-1/randomf/complete_data.csv")


# In[81]:


data


# In[82]:


def normalize(col_data):
    return (col_data - col_data.min())/(col_data.max()-col_data.min())


# In[83]:


X = data[['Yield(uM)','Yield(ug/ml)','Calculated MW(kDa)','Calculated pI', 'Sequence length', 'Sequence mass',]]
# X = data[['Yield(uM)','Yield(ug/ml)','Calculated MW(kDa)','Calculated pI', 'Type of gene product Integer']]
y = data['Solubility(%)']
for column in X:
    X.loc[:,column] = normalize(X[column])
X = round(X,2)
y = round(normalize(data.iloc[:, 1:2]),2)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# In[84]:


rf_model = RandomForestRegressor(n_estimators= 100, random_state=100)


# In[85]:


print(np.size(X_train))
print(np.shape(X_test))
print(np.shape(y_train))
print(np.shape(y_test))
print(np.shape(X_train))
y_test


# In[86]:


##rf_model.fit(X_train, y_train)
rf_model.fit(X_train, y_train.values.ravel())
predictions = rf_model.predict(X_test)


# In[87]:


print("Accuracy:",metrics.mean_squared_error(y_test, predictions))


# In[88]:


fig = plt.figure(figsize=(15, 10))
plot_tree(rf_model.estimators_[0], 
          feature_names=X.columns,
           
          filled=True, rounded=True)

plt.show()


# In[89]:



features_to_encode = X_train.columns[X_train.dtypes==object].tolist() 


# In[90]:


cat_trans = make_column_transformer(
                        (OneHotEncoder(),features_to_encode),
                        remainder = "passthrough"
                        )


# In[91]:


rforest = RandomForestClassifier(
                      min_samples_leaf=50,
                      n_estimators=150,
                      bootstrap=True,
                      oob_score=True,
                      n_jobs=-1,
                      random_state=42,
                      max_features='auto')


# In[92]:


pipe = make_pipeline(cat_trans, rforest)
pipe.fit(X_train, y_train)


# In[ ]:


y_pred = pipe.predict(X_test)


# In[ ]:


accuracy_score(y_test, y_pred)


# In[ ]:


print(f"The accuracy of the model is {round(accuracy_score(y_test,y_pred),3)*100} %")


# In[ ]:




