import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(page_title="Dashboard Qualimétrie Logicielle", layout="wide")

st.title("Dashboard de Qualimétrie Strategique")
st.markdown("Outil de pilotage basé sur l'approche **Quantitative, Qualitative et Processus**.")

# --- BARRE LATÉRALE : SAISIE DES DONNÉES ---
st.sidebar.header("Saisie des Métriques")
bugs = st.sidebar.number_input("Nombre de bugs", value=25)
loc = st.sidebar.number_input("Lignes de code (LoC)", value=8000)
couverture = st.sidebar.slider("Couverture de tests (%)", 0, 100, 75)
dette = st.sidebar.slider("Dette technique (%)", 0.0, 20.0, 12.5)
nps = st.sidebar.slider("Net Promoter Score (NPS)", -100, 100, 35)
lead_time = st.sidebar.number_input("Lead Time (jours)", value=12)

# --- CALCULS ---
taux_defauts = round(bugs / (loc / 1000), 3)

# --- AFFICHAGE DES INDICATEURS (KPIs) ---
col1, col2, col3, col4 = st.columns(4)

def check_status(value, threshold, inverse=False):
    if inverse: # Pour le NPS ou la Couverture, plus c'est haut, mieux c'est
        return "✅ Conforme" if value >= threshold else "🚨 Alerte"
    return "✅ Conforme" if value <= threshold else "🚨 Alerte"

with col1:
    st.metric("Taux de Défauts", f"{taux_defauts} b/kLoC", delta_color="inverse")
    st.write(check_status(taux_defauts, 5))

with col2:
    st.metric("Couverture Tests", f"{couverture}%")
    st.write(check_status(couverture, 80, True))

with col3:
    st.metric("Dette Technique", f"{dette}%")
    st.write(check_status(dette, 5))

with col4:
    st.metric("Lead Time", f"{lead_time} j")
    st.write(check_status(lead_time, 7))

# --- GRAPHIQUE RADAR (INTERPRÉTATION STRATÉGIQUE) ---
st.subheader("Analyse Radar : Équilibre de la Qualité")

categories = ['Fiabilité', 'Testabilité', 'Maintenabilité', 'Satisfaction', 'Efficacité']
# Normalisation simplifiée pour le graphique (0 à 100)
values = [100-(taux_defauts*10), couverture, 100-(dette*5), (nps+100)/2, 100-(lead_time*5)]

fig = go.Figure(data=go.Scatterpolar(
  r=values,
  theta=categories,
  fill='toself'
))

fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
st.plotly_chart(fig)

st.info("**Interprétation stratégique :** Ce dashboard permet de passer de l'intuition à l'action. "
        "Si une zone du radar est trop proche du centre, les ressources doivent y être réallouées en priorité.")

