# docker/Dockerfile.mlflow
FROM ghcr.io/mlflow/mlflow:v2.19.0

# On installe le driver Postgres
RUN pip install psycopg2-binary

# ON FORCE LA COMMANDE ICI
# On expose sur 0.0.0.0 pour accepter les connexions externes (Docker)
CMD mlflow server \
    --backend-store-uri postgresql://user:password@postgres:5432/mlops_db \
    --host 0.0.0.0 \
    --port 5000 \
    --default-artifact-root /mlflow/artifacts