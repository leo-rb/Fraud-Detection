import os
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score

TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
EXPERIMENT_NAME = "Fraud_Detection_Experiment"

mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment(EXPERIMENT_NAME)

print(f"📡 Tracking URI utilisée : {TRACKING_URI}")

def train():
    print("1. Calcul du chemin du fichier...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    file_path = os.path.join(project_root, "data", "creditcard.csv")
    
    if not os.path.exists(file_path):
        print(f"❌ ERREUR CRITIQUE : Fichier introuvable à : {file_path}")
        return

    print("2. Chargement de 100% des données (Ça peut prendre quelques secondes)...")
    # ON UTILISE TOUT LE DATASET MAINTENANT
    df = pd.read_csv(file_path)

    X = df.drop(['Class'], axis=1)
    y = df['Class']

    # On ajoute "stratify=y" pour garder le ratio de fraudes à l'identique dans le train et test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("3. Démarrage de l'entraînement avec équilibrage des classes...")
    
    with mlflow.start_run():
        # Hyperparamètres un peu plus costauds
        n_estimators = 100
        max_depth = 15
        
        # L'arme secrète : class_weight='balanced'
        model = RandomForestClassifier(
            n_estimators=n_estimators, 
            max_depth=max_depth, 
            class_weight='balanced',
            random_state=42,
            n_jobs=-1 # Utilise tous les cœurs du processeur pour aller plus vite
        )
        
        model.fit(X_train, y_train)
        
        # Prédictions
        predictions = model.predict(X_test)
        
        # Calcul des vraies métriques utiles
        acc = accuracy_score(y_test, predictions)
        rec = recall_score(y_test, predictions) # Capacité à trouver toutes les fraudes
        prec = precision_score(y_test, predictions) # Pertinence (pas trop de fausses alertes)
        f1 = f1_score(y_test, predictions) # Bon compromis entre Recall et Precision
        
        print(f"   📊 Accuracy  : {acc:.4f}")
        print(f"   🚨 Recall    : {rec:.4f} (Combien de vraies fraudes on a attrapé ?)")
        print(f"   🎯 Precision : {prec:.4f} (Quand on crie 'Fraude', a-t-on raison ?)")
        print(f"   ⚖️ F1-Score  : {f1:.4f}")

        # Enregistrement dans MLflow
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("class_weight", "balanced")
        
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("recall", rec)
        mlflow.log_metric("precision", prec)
        mlflow.log_metric("f1_score", f1)
        
        print("4. Sauvegarde du nouveau modèle sur le disque (Volume partagé)...")
        mlflow.sklearn.log_model(model, "fraud_detection_model")
        
        print("🎉 Entraînement V2 terminé avec succès !")

if __name__ == "__main__":
    train()