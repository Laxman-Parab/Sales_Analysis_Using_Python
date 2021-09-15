#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importing the packages

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly as px
import os


# In[2]:


#Importing the dataset

all_data = pd.read_csv(r'A:\DataScience Projects\SalesData\Sales_Data/all_data.csv')


# In[3]:


all_data.head()


# In[4]:


all_data.shape


# In[5]:


all_data.isnull().sum()


# In[6]:


#Removing null values

all_data = all_data.dropna(how = 'all')


# In[7]:


all_data.shape


# #### Which is the best month for sale?

# In[8]:


def month(x):
    return x.split('/')[0]


# In[9]:


all_data['Month'] = all_data['Order Date'].apply(month)


# In[10]:


all_data.head()


# In[11]:


all_data['Month'].unique()


# In[12]:


filter = all_data['Month']=='Order Date'              


# In[13]:


all_data = all_data[~filter]                               #To remove 'Order Date from Month column'


# In[14]:


all_data['Month'].unique()


# In[15]:


all_data['Month'] = all_data['Month'].astype(int)


# In[16]:


all_data.head()


# In[17]:


all_data['Quantity Ordered']=all_data['Quantity Ordered'].astype(int)


# In[18]:


all_data['Price Each'] = all_data['Price Each'].astype(float)


# In[19]:


all_data['Sales'] = all_data['Quantity Ordered']*all_data['Price Each']


# In[20]:


all_data.head()


# In[21]:


sum = all_data.groupby('Month')['Sales'].sum()


# In[22]:


plt.figure(figsize = (12,8))
months = range(1,13)
plt.bar(months,sum,color = 'teal')
plt.xticks(months)
plt.ylabel('Sales in USD')
plt.xlabel('Month number')
plt.show()


# The last month i.e. Decemeber has maximum sales.

# #### Which city has maximum orders?

# In[23]:


all_data.head()


# In[24]:


def city(x):
    return x.split(',')[1]


# In[25]:


all_data['City'] = all_data['Purchase Address'].apply(city)


# In[26]:


all_data.head()


# In[27]:


all_data.groupby('City')['City'].count().plot.bar()


# In[28]:


all_data.groupby('City')['City'].count()


# San Francisco has the highest number of sales followed by LA and NY city.

# #### Which product was sold the most?

# In[29]:


all_data.groupby('Product')["Quantity Ordered"].sum().plot(kind = 'bar')


# In[30]:


products=all_data.groupby('Product')['Quantity Ordered'].sum().index
quantity=all_data.groupby('Product')['Quantity Ordered'].sum()
prices=all_data.groupby('Product')['Price Each'].mean()


# In[31]:


plt.figure(figsize=(40,24))
fig,ax1 = plt.subplots()
ax2=ax1.twinx()
ax1.bar(products, quantity, color='g')
ax2.plot(products, prices, 'b-')
ax1.set_xticklabels(products, rotation='vertical', size=8)


# The top selling product is 'AAA Batteries (4-pack)'. 
# The top selling products seem to have a correlation with the price of the product. 
# The cheaper the product higher the quantity ordered.

# #### What products are most often sold together?

# In[32]:


df=all_data[all_data['Order ID'].duplicated(keep=False)]


# In[33]:


df.head()


# In[34]:


df['Combos'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))   
                                                        #Preparing new column of two products brought together based on their order id


# In[35]:


df.head()


# In[36]:


#Remove duplicate Order ID
df2 = df.drop_duplicates(subset=['Order ID'])


# In[37]:


df2.head()


# In[38]:


import plotly.graph_objs as go
from plotly.offline import iplot


# In[39]:


values=df2['Combos'].value_counts()[0:5]
labels=df['Combos'].value_counts()[0:5].index


# In[40]:


trace=go.Pie(labels=labels, values=values,
               hoverinfo='label+percent', textinfo='value', 
               textfont=dict(size=25))
iplot([trace])


# In[41]:


df2['Combos'].value_counts()[0:5].plot.pie()


# Iphone and Lightning Charging Cable are the products which were sold together more often.
