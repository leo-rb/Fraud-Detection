# Fraud Detection MLOps Pipeline

Bienvenue dans ce projet complet de détection de fraude bancaire, conçu avec une architecture MLOps robuste et conteneurisée. 

Ce projet démontre la mise en production d'un modèle de Machine Learning (Random Forest) de l'entraînement jusqu'au déploiement via une API REST et une interface utilisateur interactive.

graph TD
    %% Définition des styles
    classDef storage fill:#f9f,stroke:#333,stroke-width:2px;
    classDef compute fill:#bbf,stroke:#333,stroke-width:2px;
    classDef interface fill:#dfd,stroke:#333,stroke-width:2px;
    classDef user fill:#fff,stroke:#333,stroke-width:4px;

    %% Les Acteurs et Données Extérieures
    Utilisateur((Recruteur / <br/>Manager)):::user
    Dataset(Kaggle: <br/>creditcard.csv):::storage

    %% Le Réseau Docker (Frontière virtuelle)
    subgraph DockerNet[Réseau Virtuel Docker Compose]
        direction TB

        %% Bloc Stockage
        subgraph Stockage[Persistance des Données]
            Postgres[(🐘 PostgreSQL <br/> Métadonnées MLflow)]:::storage
            Volume[(📂 Volume Partagé <br/> Artefacts Modèles)]:::storage
        end

        %% Bloc MLOps
        subgraph MLOps[Tracking & Registry]
            MLflow(📈 Serveur MLflow <br/> Tracking Experimentations):::compute
        end

        %% Bloc Entraînement
        subgraph Calcul[Pipeline ML]
            Trainer[🐍 Script Python <br/> Entraînement & SMOTE]:::compute
        end

        %% Bloc Inférence (Production)
        subgraph Production[Zone de Service]
            API[⚡ FastAPI <br/> Serveur d'Inférence]:::compute
            Streamlit[🎨 Interface Streamlit <br/> Web App]:::interface
        end
    end

    %% Les Flux Logiques (Les flèches)
    Dataset -.->|1. Manuel| Trainer
    Utilisateur ==>|2. docker-compose up| DockerNet
    
    %% Flux Entraînement
    Trainer -->|3a. Log Métriques| MLflow
    MLflow -->|3b. Sauvegarde| Postgres
    Trainer -->|3c. Sauvegarde .pkl| Volume
    
    %% Flux Inférence
    API -->|4a. Charge modèle| Volume
    API -.->|4b. Vérifie Registry| MLflow
    Utilisateur ==>|5. Teste la fraude| Streamlit
    Streamlit ==>|6. Requête POST| API
    API ==>|7. Prédiction JSON| Streamlit

    %% Légende masquée pour styles
    %% class Dataset,Postgres,Volume storage;
    %% class MLflow,Trainer,API compute;
    %% class Streamlit interface;

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
