# Fraud Detection MLOps Pipeline

Bienvenue dans ce projet complet de détection de fraude bancaire, conçu avec une architecture MLOps robuste et conteneurisée. 

Ce projet démontre la mise en production d'un modèle de Machine Learning (Random Forest) de l'entraînement jusqu'au déploiement via une API REST et une interface utilisateur interactive.

```
graph TD
    %% Acteurs extérieurs
    User(("👤 Recruteur / Utilisateur"))
    Data[("📁 creditcard.csv (Kaggle)")]

    subgraph "Infrastructure Docker (Réseau mlops_net)"
        direction TB
        
        subgraph "1. Zone de Données & Tracking"
            DB[("🐘 PostgreSQL (Métadonnées)")]
            Volume[("📂 Volume Local (Modèles .pkl)")]
            MLflow("📈 Serveur MLflow")
        end
        
        subgraph "2. Zone d'Entraînement"
            Trainer("🐍 Script d'Entraînement (train.py)")
        end
        
        subgraph "3. Zone de Production"
            API("⚡ API REST (FastAPI)")
            UI("🎨 Interface Web (Streamlit)")
        end
    end

    %% Flux d'exécution
    Data -.->|"Ajout manuel"| Trainer
    User ==>|"docker-compose up"| UI
    
    Trainer -->|"1. Log des métriques"| MLflow
    MLflow -->|"2. Sauvegarde"| DB
    Trainer -->|"3. Enregistre le modèle"| Volume
    
    API -->|"4. Charge le modèle"| Volume
    API -.->|"5. Vérifie le registre"| MLflow
    
    UI ==>|"6. Envoie les 30 features"| API
    API ==>|"7. Retourne la prédiction"| UI
```

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
git clone [https://github.com/leo-rb/Fraud-Detection.git](https://github.com/leo-rb/Fraud-Detection.git)
cd Fraud-Detection
```
**2. Ajouter les données**

Note : Le dataset complet (144 Mo) n'est pas versionné sur GitHub.

Téléchargez le dataset creditcard.csv depuis Kaggle - Credit Card Fraud Detection.

Placez le fichier creditcard.csv dans le dossier data/ à la racine du projet.

**3. Démarrer l'infrastructure**
```bash
docker-compose up -d
```
Docker va automatiquement construire les images, démarrer la base de données, lancer le serveur MLflow, entraîner le modèle, et exposer l'API et l'interface Web.

## Accès aux interfaces ##

Une fois les conteneurs démarrés, vous pouvez accéder aux services suivants depuis votre navigateur :

Interface Utilisateur (Streamlit) : http://localhost:8501

Tracking MLflow : http://localhost:5000

API REST (FastAPI / Swagger UI) : http://localhost:8000/docs

## Nettoyage ##

Pour éteindre et supprimer les conteneurs proprement :

```bash
docker-compose down
```
