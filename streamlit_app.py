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
new_column_names_salaire = {
    'SNHM14': 'salaire',
    'SNHMC14': 'salaire_cadre',
    'SNHMP14': 'salaire_cadre_moyen',
    'SNHME14': 'salaire_employe',
    'SNHMO14': 'salaire_travailleur',
    'SNHMF14': 'salaire_femme',
    'SNHMFC14': 'salaire_cadre_femme',
    'SNHMFP14': 'salaire_cadre_moyen_femme',
    'SNHMFE14': 'salaire_employe_femme',
    'SNHMFO14': 'salaire_travailleur_femme',
    'SNHMH14': 'salaire_homme',
    'SNHMHC14': 'salaire_cadre_homme',
    'SNHMHP14': 'salaire_cadre_moyen_homme',
    'SNHMHE14': 'salaire_employe_homme',
    'SNHMHO14': 'salaire_travailleur_homme',
    'SNHM1814': 'salaire_18-25',
    'SNHM2614': 'salaire_26-50',
    'SNHM5014': 'salaire_+50',
    'SNHMF1814': 'salaire_18-25_femme',
    'SNHMF2614': 'salaire_26-50_femme',
    'SNHMF5014': 'salaire_+50_femme',
    'SNHMH1814': 'salaire_18-25_homme',
    'SNHMH2614': 'salaire_26-50_homme',
    'SNHMH5014': 'salaire_+50_homme'
}

# Renommer les colonnes du dataframe salaire
salaire = salaire.rename(columns=new_column_names_salaire)

# Supprimer les zéros en première position
salaire['CODGEO'] = salaire['CODGEO'].str.lstrip('0')

# Remplacer les lettres A ou B par des zéros
salaire['CODGEO'] = salaire['CODGEO'].str.replace('A', '0').str.replace('B', '0')

# Afficher les données chargées
st.write("Colonnes du dataset 'etablissement' :")
st.write(etablissement.columns)
st.write("Colonnes du dataset 'geographic' :")
st.write(geographic.columns)
# st.write("Colonnes du dataset 'population' :")
# st.write(population.columns)
st.write("Colonnes du dataset 'salaire' :")
st.write(salaire.columns)

# Afficher un aperçu des données
st.write("Aperçu des données 'etablissement' :")
st.dataframe(etablissement.head(10))

st.write("Aperçu des données 'geographic' :")
st.dataframe(geographic.head(10))

# st.write("Aperçu des données 'population' :")
# st.dataframe(population.head(10))

st.write("Aperçu des données 'salaire' :")
st.dataframe(salaire.head(10))

# Afficher les informations sur les datasets
st.write("Information sur les données 'etablissement' :")
buffer = io.StringIO()
etablissement.info(buf=buffer)
s = buffer.getvalue()
st.text(s)

st.write("Information sur les données 'geographic' :")
buffer = io.StringIO()
geographic.info(buf=buffer)
s = buffer.getvalue()
st.text(s)

# st.write("Information sur les données 'population' :")
# buffer = io.StringIO()
# population.info(buf=buffer)
# s = buffer.getvalue()
# st.text(s)

st.write("Information sur les données 'salaire' :")
buffer = io.StringIO()
salaire.info(buf=buffer)
s = buffer.getvalue()
st.text(s)
