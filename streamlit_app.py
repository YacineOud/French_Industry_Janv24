import streamlit as st
import pandas as pd

# URL du fichier CSV
csv_url = "https://raw.githubusercontent.com/ChristopheMontoriol/French_Industry_Janv24/main/data/base_etablissement_par_tranche_effectif.csv"

# Lecture du CSV
@st.cache_data
def load_data(url):
    return pd.read_csv(url, sep=',')

# Chargement des données
data = load_data(csv_url)

# Affichage des 10 premières lignes
st.title("Affichage des 10 premières lignes du CSV")
st.write(data.head(10))
