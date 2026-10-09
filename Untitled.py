#!/usr/bin/env python
# coding: utf-8

# In[42]:

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# In[43]:


netflix=pd.read_csv("netflix.csv")


# In[44]:


netflix


# In[45]:


# data cleaning 

netflix.shape #is use for find how many rows and columns in dataset 


# In[46]:


netflix.info() # is use for find all information of data like data type and null value 


# In[47]:


netflix.isnull().sum() # to check total  null values in data 


# In[48]:


netflix.duplicated().sum()


# In[49]:


netflix.describe() #  is used for see statastical information in dataset


# In[50]:


netflix["Watch_Date"]=pd.to_datetime(netflix["Watch_Date"])


# In[51]:


netflix.info()


# In[52]:


netflix.dtypes


# In[57]:


netflix.groupby("Region")["Monthly_Revenue"].sum().plot(kind="bar",ylabel="Monthly_Revenue",title="region wise revenue")


# In[61]:


netflix.groupby("Subscription_Plan")["Rating"].sum().plot(kind="pie",title="subscription plan wise rating")


# In[64]:


netflix["Rating"].value_counts().plot(kind="bar")


# In[68]:


netflix.groupby("Category")["Monthly_Revenue"].sum().plot(kind="pie",title="category wise revenue")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




