import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import io

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Pour éviter d'avoir les messages warning
import warnings
warnings.filterwarnings('ignore')

# Titre de l'application
st.title('Import des DataSets')

# Charger les données
# Charger les données
@st.cache_data
def load_data():
    etablissement_url = 'https://github.com/ChristopheMontoriol/French_Industry_Janv24/blob/main/data/base_etablissement_par_tranche_effectif.csv'
    geographic_url = 'https://github.com/ChristopheMontoriol/French_Industry_Janv24/blob/main/data/name_geographic_information.csv'
    # population_url = 'https://github.com/ChristopheMontoriol/French_Industry_Janv24/blob/main/data/population.csv'
    salaire_url = 'https://github.com/ChristopheMontoriol/French_Industry_Janv24/blob/main/data/net_salary_per_town_categories.csv'
    
    etablissement = pd.read_csv(etablissement_url, sep=',')
    geographic = pd.read_csv(geographic_url, sep=',')
    # population = pd.read_csv(population_url, sep=',')
    salaire = pd.read_csv(salaire_url, sep=',')
    return etablissement, geographic, salaire

etablissement, geographic, salaire = load_data()

# Pré-processing
# ---------------------------------------------------------------------------------------------------------------
# PREPARATION DU DATAFRAME SALAIRE
# ---------------------------------------------------------------------------------------------------------------
# Dictionnaire de correspondance entre anciens et nouveaux noms de colonne du dataframe salaire

