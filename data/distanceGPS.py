
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

from math import sin, cos, acos, pi

pd.options.display.max_rows = 8
#%%


#Importation des données qui nous permattra de calculer les distances 
#%%
data_dist = pd.read_csv('DataFrame_dist.csv', sep = ',', header = 0)
data_dist
#%%