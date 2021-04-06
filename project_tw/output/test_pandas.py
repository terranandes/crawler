#!/usr/bin/env python
# coding: utf-8

# In[3]:


import json
import pandas as pd
with open('stock_list_s2006e2021.json', 'r', encoding='utf-8') as fh:
  sd = json.load(fh)

print(sd)

# In[4]:


#df = pd.DataFrames(sd)


# 
