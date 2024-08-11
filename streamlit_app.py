
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import seaborn as sns
import plotly.express as px
from io import StringIO
import requests
from io import BytesIO
from PIL import Image
from scipy.stats import normaltest
from scipy.stats import norm
import pickle
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import statsmodels.api as sm
import io


# Pour éviter d'avoir les messages warning
import warnings
warnings.filterwarnings('ignore')


# Charger les données
@st.cache_data
def load_data():
    etablissement_url = 'https://raw.githubusercontent.com/ChristopheMontoriol/French_Industry_Janv24/main/data/base_etablissement_par_tranche_effectif.csv'
    geographic_url = 'https://raw.githubusercontent.com/ChristopheMontoriol/French_Industry_Janv24/main/data/name_geographic_information.csv'
    # population_url = 'https://raw.githubusercontent.com/ChristopheMontoriol/French_Industry_Janv24/main/data/population.csv'
    salaire_url = 'https://raw.githubusercontent.com/ChristopheMontoriol/French_Industry_Janv24/main/data/net_salary_per_town_categories.csv'
    
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


# Configuration de la barre latérale
st.sidebar.title("Sommaire")
pages=["👋 Intro", "🔍 Exploration des données", "📊 Data Visualisation", "🧩 Modélisation", "🔮 Prédiction", "📌Conclusion"]
page=st.sidebar.radio("Aller vers", pages)
st.sidebar.markdown(
    """
    - **Cursus** : Data Analyst
    - **Formation** : Formation Continue
    - **Mois** : Janvier 2024
   - **Groupe** : 
        - Christophe MONTORIOL
        - Issam YOUSR
        - Gwilherm DEVALLAN
        - Yacine OUDMINE""")

####################################################################################################
# Page d'introduction
####################################################################################################



if page == pages[0] :
    
    # Présentation projet
    st.caption("""**Cursus** : Data Analyst
    | **Formation** : Formation Continue
    | **Mois** : Janvier 2024
    | **Groupe** : Christophe MONTORIOL,Issam YOUSR,Gwilherm DEVALLAN,Yacine OUDMINE
        """)


    st.header("👋 Intro")
    st.markdown("""<style>h1 {color: #4629dd;  font-size: 70px;/* Changez la couleur du titre h1 ici */} h2 {color: #440154ff;    font-size: 50px /* Changez la couleur du titre h2 ici */} h3{color: #27dce0; font-size: 30px; /* Changez la couleur du titre h3 ici */}</style>""",unsafe_allow_html=True)
    st.markdown("""<style>body {background-color: #f4f4f4;</style>""",unsafe_allow_html=True)

    st.write(  """
    L’objectif premier de ce projet est d’observer et de comprendre quelles sont les inégalités salariales en France.
    À travers plusieurs jeux de données et plusieurs variables (géographiques, socio-professionnelles, démographiques, mais aussi du nombre d’entreprises par zone), 
    il sera question dans ce projet de mettre en lumière les facteurs d’inégalités les plus déterminants et de recenser ainsi les variables qui ont un impact significatif sur les deltas de salaire.

    En plus de distinguer les variables les plus déterminantes sur les niveaux de revenus, l’objectif de cette étude sera de construire des clusters ou des groupes de pairs. 
    Ces groupes seront fondés sur la base des revenus de ces individus ayant des niveaux de salaire proches.  
    
    Enfin, au-delà d’un travail d'observation et d’analyse statistique, le second volet de ce projet s’articulera autour de la création d’un modèle de Machine Learning capable de prédire le plus finement possible 
    un salaire en fonction des différentes variables à disposition dans ces jeux de données.
    """)

    
            
####################################################################################################
# Page d'exploration des données
####################################################################################################

if page == pages[1] : 
    #st.header("🔍 Exploration des Données")
    st.markdown("""<style>h1 {color: #4629dd;  font-size: 70px;/* Changez la couleur du titre h1 ici */} h2 {color: #440154ff;    font-size: 50px /* Changez la couleur du titre h2 ici */} h3{color: #27dce0; font-size: 30px; /* Changez la couleur du titre h3 ici */}</style>""",unsafe_allow_html=True)
    st.markdown("""<style>body {background-color: #f4f4f4;</style>""",unsafe_allow_html=True)


    # Gestion de l'état de la page via session_state
    if 'page' not in st.session_state:
        st.session_state.page = "Etablissement"

    # Sélection de la page
    pages = ["Etablissement", "Geographic", "Salaire"]
    st.session_state.page = st.sidebar.selectbox("Choisissez la page", pages, index=pages.index(st.session_state.page))

    # Ajout de styles personnalisés
    st.markdown("""
        <style>
            h1 {color: #4629dd; font-size: 70px;}
            h2 {color: #440154ff; font-size: 50px;}
            h3 {color: #27dce0; font-size: 30px;}
            body {background-color: #f4f4f4;}
        </style>
    """, unsafe_allow_html=True)

    # Fonction pour afficher les informations des DataFrames
    def afficher_info(dataframe, name):
        st.write(f"### {name}")
        st.write("#### .head()")
        st.write(dataframe.head())
        
        st.write("#### .info()")
        buffer = io.StringIO()
        dataframe.info(buf=buffer)
        st.text(buffer.getvalue())
        
        st.write("#### .describe()")
        st.write(dataframe.describe())

    # Affichage des informations en fonction de la page sélectionnée
    if st.session_state.page == "Etablissement":
        st.header("🔍 Exploration des Données - Etablissement")
        afficher_info(etablissement, "Etablissement")
        if st.button("Voir Geographic"):
            st.session_state.page = "Geographic"
        if st.button("Voir Salaire"):
            st.session_state.page = "Salaire"

    elif st.session_state.page == "Geographic":
        st.header("🔍 Exploration des Données - Geographic")
        afficher_info(geographic, "Geographic")
        if st.button("Voir Etablissement"):
            st.session_state.page = "Etablissement"
        if st.button("Voir Salaire"):
            st.session_state.page = "Salaire"

    elif st.session_state.page == "Salaire":
        st.header("🔍 Exploration des Données - Salaire")
        afficher_info(salaire, "Salaire")
        if st.button("Voir Etablissement"):
            st.session_state.page = "Etablissement"
        if st.button("Voir Geographic"):
            st.session_state.page = "Geographic"



####################################################################################################
#  Data Viz
####################################################################################################


if page == pages[2] :
    st.markdown("""<style>h1 {color: #4629dd;  font-size: 70px;/* Changez la couleur du titre h1 ici */} h2 {color: #440154ff;    font-size: 50px /* Changez la couleur du titre h2 ici */} h3{color: #27dce0; font-size: 30px; /* Changez la couleur du titre h3 ici */}</style>""",unsafe_allow_html=True)
    st.markdown("""<style>body {background-color: #f4f4f4;</style>""",unsafe_allow_html=True)

    st.header("📊 Data Visualisation")
       
####################################################################################################
# Modèle de machine Learning
####################################################################################################



if page == pages[4]:
    st.header("🔮 Prédiction")
    st.markdown("""<style>h1 {color: #4629dd;  font-size: 70px;/* Changez la couleur du titre h1 ici */} h2 {color: #440154ff;    font-size: 50px /* Changez la couleur du titre h2 ici */} h3{color: #27dce0; font-size: 30px; /* Changez la couleur du titre h3 ici */}</style>""",unsafe_allow_html=True)
    st.markdown("""<style>body {background-color: #f4f4f4;</style>""",unsafe_allow_html=True)

    # Interface utilisateur Streamlit
    st.subheader('Simulation de Prédiction avec Random Forest Regressor')


    
####################################################################################################
# Conclusion
####################################################################################################


if page == pages[5]:
    st.header("📌 Conclusion")
    st.markdown("""<style>h1 {color: #4629DD;  font-size: 70px;/* Changez la couleur du titre h1 ici */} h2 {color: #440154ff;    font-size: 50px /* Changez la couleur du titre h2 ici */} h3{color: #27DCE0; font-size: 30px; /* Changez la couleur du titre h3 ici */}</style>""",unsafe_allow_html=True)
    st.markdown("""<style>body {background-color: #F4F4F4;</style>""",unsafe_allow_html=True)
    st.write("**Conclusion**")

      #  if st.button("Merci") :
      #  st.write("Nous souhaiterions remercier pour nous avoir aidé sur ce projet :")
      #  st.write("- Notre mentor sur le projet Tarik Anouar,")
      #  st.write("- DataScientest dont les animateurs des masterclasses ")
      #  st.write("- Les données trouvées sur Kaggle,")
      # st.write("- ... ChatGPT!")
