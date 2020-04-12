# %%
# import and initialization examples
import graphviz
import seaborn as sns
from IPython import get_ipython

import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

get_ipython().run_line_magic("matplotlib", "inline")  # same as matplotlib inline
pd.options.mode.chained_assignment = None  # default='warn'

sns.set()
plt.style.use("seaborn-colorblind")

# %%
df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)


names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')


# %%
df.iloc[0]

# %%
df['Gold'].idxmax()
# %%
abs(df['Gold']-df['Gold.1']).idxmax()

# %%
df['Gold.2']*3+df['Silver.2']*2+df['Bronze.2']

# %%
census_df = pd.read_csv('census.csv')

census_df[census_df['SUMLEV'] == 50].set_index(['STNAME', 'COUNTY'])['SUMLEV'].count(level=0).idxmax()

# %%
census_df[census_df['SUMLEV'] == 50].set_index('STNAME').sort_values(by=['STNAME','CENSUS2010POP'], ascending=[True,False]).groupby(level=0).head(3)['CENSUS2010POP'].sum(level=0).sort_values(ascending=False)[0:3].index.values.tolist()

# %%
