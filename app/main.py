import os
import mlflow.sklearn
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# On force le flush des prints pour voir les logs dans Docker tout de suite
import sys

app = FastAPI()

# Modèle global
model = None

# Définition du format des données d'entrée
class FraudDetectionRequest(BaseModel):
    features: List[float]

@app.on_event("startup")
def load_model():
    global model
    # On récupère l'IP magique depuis docker-compose
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
    experiment_name = "Fraud_Detection_Experiment"
    
    print(f"🔌 Tentative de connexion à MLflow sur : {tracking_uri}", flush=True)
    mlflow.set_tracking_uri(tracking_uri)
    
    try:
        # On cherche la dernière exécution réussie
        client = mlflow.tracking.MlflowClient()
        experiment = client.get_experiment_by_name(experiment_name)
        
        if experiment is None:
            print("❌ L'expérience n'existe pas encore.", flush=True)
            return

        runs = client.search_runs(
            experiment_ids=[experiment.experiment_id],
            filter_string="tags.mlflow.source.type = 'LOCAL'",
            order_by=["attribute.start_time DESC"],
            max_results=1
        )
        
        if not runs:
            print("⚠️ Aucun run trouvé.", flush=True)
            return
            
        run_id = runs[0].info.run_id
        model_uri = f"runs:/{run_id}/fraud_detection_model"
        
        print(f"📥 Chargement du modèle depuis : {model_uri}", flush=True)
        model = mlflow.sklearn.load_model(model_uri)
        print("🚀 Modèle chargé en mémoire avec succès !", flush=True)
        
    except Exception as e:
        print(f"❌ Erreur critique lors du chargement du modèle : {e}", flush=True)

@app.post("/predict")
def predict(request: FraudDetectionRequest):
    global model
    if model is None:
        # On réessaie de charger si c'était vide (lazy loading)
        print("⚠️ Modèle vide, tentative de rechargement...", flush=True)
        load_model()
        if model is None:
            raise HTTPException(status_code=503, detail="Modèle non chargé. Vérifiez les logs API.")

    try:
        # Transformation en DataFrame
        data = pd.DataFrame([request.features])
        prediction = model.predict(data)
        return {"fraud_prediction": int(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def read_root():
    status = "Actif 🟢" if model else "Inactif 🔴 (Modèle non chargé)"
    return {"status": "API Fraud Detection", "model_state": status}