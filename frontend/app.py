import streamlit as st
import requests

st.set_page_config(page_title="Détection de Fraude", page_icon="🚨")

st.title("🚨 Détecteur de Fraude Bancaire")
st.write("Saisissez les 30 caractéristiques (features) de la transaction pour vérifier si elle est frauduleuse.")

# On génère une liste de 30 zéros par défaut pour faciliter le test
default_features = [0.0] * 30
default_text = ", ".join(map(str, default_features))

st.subheader("Données de la transaction")
user_input = st.text_area("Features (30 nombres séparés par des virgules)", value=default_text, height=100)

if st.button("🔮 Prédire", type="primary"):
    try:
        # Nettoyage et conversion de l'entrée utilisateur
        features = [float(x.strip()) for x in user_input.split(',')]
        
        if len(features) != 30:
            st.warning(f"⚠️ Il faut exactement 30 nombres. Vous en avez entré {len(features)}.")
        else:
            with st.spinner("Analyse en cours..."):
                # On envoie les données à ton API interne via le réseau Docker (http://api:8000)
                response = requests.post("http://api:8000/predict", json={"features": features})
                
                if response.status_code == 200:
                    result = response.json()["fraud_prediction"]
                    if result == 1:
                        st.error("🚨 ALERTE : Transaction potentiellement FRAUDULEUSE !")
                    else:
                        st.success("✅ Transaction normale autorisée.")
                else:
                    st.error(f"Erreur de l'API : {response.text}")
                    
    except ValueError:
        st.error("❌ Erreur : Veuillez ne saisir que des nombres séparés par des virgules.")
    except requests.exceptions.ConnectionError:
        st.error("🔌 Impossible de joindre l'API. Est-elle bien démarrée ?")