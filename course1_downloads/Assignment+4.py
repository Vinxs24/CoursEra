
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[ ]:

# When using loc
# df.loc[:] = Dataframe

# df.loc[int] = Dataframe if you have more than one column and Series if you have only 1 column in the dataframe

# df.loc[:, ["col_name"]] = Dataframe

# df.loc[:, "col_name"] = Series

# Not using loc
# df["col_name"] = Series

# df[["col_name"]] = Dataframe


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

racine ='C:\\Users\\vince\\Documents\\Python Scripts\\CoursEra_Pythonetdatasciene_1\\course1_downloads\\'
file = racine + 'City_Zhvi_AllHomes.csv'
file2 = racine + 'university_towns.txt'
file3 = racine + 'gdplev.xls'

# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[ ]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[ ]:


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    univ = pd.read_csv(file2, sep='|',header=None)
    univ.columns=['RegionName']
    # Regrouper en ut=pd.read_csv('university_towns.txt', sep='|', header=None, names=['RegionName'])
    
    univ['State']=univ['RegionName'].str.find('[edit]')
    
    # Pour éviter une boucle for et faciliter le remplissage ut['State'].fillna(method='ffill', inplace=True)
    
    A = univ['State'].copy()   
    for i in range(0, len(univ['State'])):
        if univ['State'].iloc[i]>0:
            StateName = univ['RegionName'].iloc[i]
        else:
            A[i] = StateName
    
    univ['State'] = A.str.replace('\[.*','') # Je le fais en deux fois pour éviter un warning sur les copy et view
    #ut['State']=ut['State'].str.extract('(.*)(?:\[edit\])$')
    univ = univ[univ['RegionName'].str.find('[edit]')<0]
    #ut = ut[ut['RegionName'].str.match('(?!.*\[edit\]$)')]
    
    univ['RegionName']=univ['RegionName'].str.replace(' \(.*|:','')
    univ=univ.reindex(columns=['State','RegionName'])
    return univ


# In[ ]:

    gpd = pd.read_excel(file3,usecols = "E:G",header = 5).dropna().rename(columns={'Unnamed: 4':'Period','GDP in billions of current dollars.1':'GDP current','GDP in billions of chained 2009 dollars.1':'GDP chained'})
gpd=gpd[gpd['Period']>'2000']

# df=pd.read_excel('gdplev.xls', skiprows=list(range(5))+[6,7], usecols=list(range(3))+list(range(4,7)))

def get_recession_start():
    
    Recess =gpd[(gpd['GDP chained'].diff()<0) & (gpd['Diff'].shift(-1)<0)]
           
    return Recess.iloc[0].loc['Period']

# Pour reset index: quarters2000.reset_index(inplace=True, drop=True)

# In[ ]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    
    gpd.loc[gpd['Period'] == get_recession_start()].index[0]
    
    for i in range(gpd.loc[gpd['Period'] == get_recession_start()].index[0],gpd.index[len(gpd)-1]): #ou bien réindexer le df depuis le début
        if (gpd['GDP chained'].diff()[i]>0) & (gpd['Diff'].shift(+1)[i]>0):
            res = i
            break
  
    return gpd.loc[res].loc['Period']


# In[ ]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    debut = gpd.loc[gpd['Period'] == get_recession_start()].index[0]
    fin = gpd.loc[gpd['Period'] == get_recession_end()].index[0]
    
    ind = gpd.loc[debut:fin,:]['GDP chained'].idxmin()
    
    return gpd.loc[ind].loc['Period']


# In[ ]:


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    df = pd.read_csv(file)
    df.replace(to_replace=states, value=None, inplace = True)
    
    cols= df.loc[:,'1996-04':'1999-12'].columns
    df=df.set_index(["State","RegionName"]).drop(columns=cols)
    
    df.columns = df.columns.str.replace('-0[1-3]','q1').str.replace('-0[4-6]','q2').str.replace('-0[7-9]','q3').str.replace('-1[0-2]','q4')
    
    df = df.loc[:,'2000q1':].groupby(level=0, axis = 1).mean()  
    # Je n'avais initialement pas mis le .loc d'où l'erreur sur les valeurs numériques.
    #df = df.groupby(level=0, axis = 1).mean()
    
    
    ##### GRRRRRRRRRRRRRRRRRR j'en peux plus des groupby...
   # https://stackoverflow.com/questions/25736127/pandas-groupby-with-dict
    
    # Soluce Gabi
    # df=pd.read_csv('City_Zhvi_AllHomes.csv', encoding = "ISO-8859-1")
    # groupby_dict={}
    # for i in range(0,17):
    #     for j in range(1,13):
    #         if(j<=3):
    #             groupby_dict[(str(2000+i)+ '-'+'{:0>2d}'.format(j))]=(str(2000+i)+ 'q1')
    #         elif(j<=6):
    #             groupby_dict[(str(2000+i)+ '-'+'{:0>2d}'.format(j))]=(str(2000+i)+ 'q2')
    #         elif(j<=9):
    #             groupby_dict[(str(2000+i)+ '-'+'{:0>2d}'.format(j))]=(str(2000+i)+ 'q3')
    #         else:
    #             groupby_dict[(str(2000+i)+ '-'+'{:0>2d}'.format(j))]=(str(2000+i)+ 'q4')

    
    # return df.set_index(['State','RegionName']).loc[:,'2000-01':].groupby(groupby_dict,axis=1).mean()

    return "ANSWER"


# In[ ]:


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    # ut=get_list_of_university_towns().set_index(['State', 'RegionName'])
    # ut['University Town']=True

    # df=convert_housing_data_to_quarters()
    # df=df.loc[:,get_recession_start():get_recession_end()]

    # comb = df.merge(ut,how='left',right_index=True,left_index=True)
    # comb['University Town']=comb['University Town'].fillna(False)

    # university=comb[comb['University Town']==True]
    # nonuniversity=comb[comb['University Town']==False]
    # university_decline=university.iloc[:,-2]-university.iloc[:,0]
    # nonuniversity_decline=nonuniversity.iloc[:,-2]-nonuniversity.iloc[:,0]
    # univ_dec_ratio=university_decline.mean()/university.iloc[:,0].mean()
    # nonuniv_dec_ratio=nonuniversity_decline.mean()/nonuniversity.iloc[:,0].mean()
    # better = ('university-town' if univ_dec_ratio>nonuniv_dec_ratio else 'non-university-town')
    # (stat,p)=ttest_ind(university_decline, nonuniversity_decline,nan_policy='omit')
    # different = (True if p<0.01 else False)
    
    return "ANSWER"

