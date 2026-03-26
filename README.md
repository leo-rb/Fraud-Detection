# Fraud Detection MLOps Pipeline

Bienvenue dans ce projet complet de détection de fraude bancaire, conçu avec une architecture MLOps robuste et conteneurisée. 

Ce projet démontre la mise en production d'un modèle de Machine Learning (Random Forest) de l'entraînement jusqu'au déploiement via une API REST et une interface utilisateur interactive.

## Architecture Technique

Le projet repose sur 5 services interconnectés via Docker :
* **PostgreSQL** : Base de données relationnelle pour stocker les métadonnées des modèles.
* **MLflow** : Serveur de tracking d'expérimentations et registre de modèles.
* **Entraînement (Script)** : Pipeline de traitement de données (SMOTE pour le déséquilibre de classes) et entraînement du modèle.
* **FastAPI** : API REST qui charge dynamiquement le meilleur modèle depuis MLflow pour effectuer des prédictions.
* **Streamlit** : Interface web utilisateur pour tester le modèle en temps réel.

## Prérequis

* [Docker](https://www.docker.com/products/docker-desktop/) et Docker Compose installés sur votre machine.
* Git.

## Comment lancer le projet (Plug & Play)

**1. Cloner le dépôt**
```bash
git clone [https://github.com/VOTRE_NOM/Fraud-Detection.git](https://github.com/VOTRE_NOM/Fraud-Detection.git)
cd Fraud-Detection

**2. Ajouter les données**
Note : Le dataset complet (144 Mo) n'est pas versionné sur GitHub.

Téléchargez le dataset creditcard.csv depuis Kaggle - Credit Card Fraud Detection.

Placez le fichier creditcard.csv dans le dossier data/ à la racine du projet.
