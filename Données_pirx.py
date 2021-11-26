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

#%%
price=pd.read_csv('DataFrame_price.csv',sep=';', header=0)
price
#%%

#énumération des colonnes
#%%

print(price.columns)

#%%

#Affichage des 5 premières lignes de la Dataprice
#%%
print(price.head())
#%%

#description of dataprice
#%%
print(price.describe(include = 'all'))
print(price.info())
#%%
#
#%%

#price = price.apply(lambda x: x.fillna(x.value_counts().index())
#%%
# On remplace les valeurs manquantes par la median
#%%
price.fillna(price.mean())

#price.apply( lambda x: x.fillna(x.median()), axis=0)

#%%

#%%
median = price['Peage de Montpellier St-Jean'].median()
price['Peage de Montpellier St-Jean'].fillna(median, inplace=True)
price
median = price['Peage de Toulouse sud/est'].median()
price['Peage de Toulouse sud/est'].fillna(median, inplace=True)

median = price['St-Jean-de-Vedas'].median()
price['St-Jean-de-Vedas'].fillna(median, inplace=True)
price
#%%
print(price.isnull())
#%%

#Affichage des prix des péages de la villes Vendargues

#%%
plt.figure(figsize=(5, 5))
plt.hist(price['Sesquieres'], density=True, bins=25)
plt.xlabel('Sesquieres')
plt.ylabel('Proportion')
plt.title("le prix des péages de Sesquieres")
#%%

#
#%%
plt.figure(figsize=(5, 5), num='jfpwje')
# KDE: kernel density estimate
ax = sns.kdeplot(price['Sesquieres'], shade=True, cut=0, bw=0.1)  # bw: bandwith
plt.xlabel('Proportion')
plt.ylabel('Sesquieres')
ax.legend().set_visible(False)
plt.title("le prix des péages density estimate")
plt.tight_layout()


#%%





#%%
def hist_explore(
    dataset=price,
    variable=price.columns,
    n_bins=24,
    alpha=0.25,
    density=False,
):
    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    ax.hist(
        dataset[variable], density=density, bins=n_bins, alpha=alpha
    )  # standardization
    plt.ylabel("Density level")
    plt.title(f"Dataset {dataset.attrs['name']}:\n Histogram for' Sesquieres")
    plt.tight_layout()
    plt.show()


interact(
    hist_explore,
    dataset=fixed(price),
    n_bins=(1, 50, 1),
    alpha=(0, 1, 0.1),
    density=False,
)
def kde_explore(dataset=price, variable=price.columns, bw=5):
    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    sns.kdeplot(dataset[variable], bw_adjust=bw, shade=True, cut=0, ax=ax)
    plt.ylabel("Density level")
    plt.title(f"Dataset {dataset.attrs['name']}:\n KDE for passengers'  {variable}")
    plt.tight_layout()
    plt.show()

interact(kde_explore, dataset=fixed(price), bw=(0.001, 2, 0.01))

#%%