#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from functools import partial
from pyproj import CRS
from pyproj import Proj, transform
# widget manipulation
from ipywidgets import widgets, interact, interactive, fixed, interact_manual

from download import download  # download data / avoid re-downloading
from IPython import get_ipython

pd.options.display.max_rows = 8
#%%

# Importation de la base des données des prix que nous avons crée à partir d'Excel

#%%
price = pd.read_csv('DataFrame_price.csv',sep=';', header=0)
price
#%%

#description de la base des données 

#%%
print(price.describe(include = 'all'))
print(price.info())
#%%

# On remplace les valeurs manquantes par la médiane

#%%
price.fillna(price.mean())

#price.apply( lambda x: x.fillna(x.median()), axis=0)

#%%

#%%

print(price.isnull())
#%%

