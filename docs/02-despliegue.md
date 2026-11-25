# 2. Guía de despliegue

## 2.1 Requisitos

- Cuenta de GitHub y de OpenCellID (token).
- Suscripción de Azure.
- GitHub Codespaces (recomendado), o Docker, kind, kubectl, Azure CLI, GitHub CLI y Terraform 1.9+.
- Archivo de datos de Colombia en `data/732.csv.gz`. No se sube al repositorio.

## 2.2 Local con Docker Compose

```bash
cp .env.example .env
sed -i "s/cambia-esta-clave/$(openssl rand -hex 16)/" .env
docker compose up -d --build
docker compose run --rm ingestor python ingest.py /data/732.csv.gz
curl http://localhost:8000/ready
```

- Web: <http://localhost:8080>
- Documentación de la API: <http://localhost:8000/docs>

En Git Bash para Windows, antepón `MSYS_NO_PATHCONV=1` al comando del ingestor.

## 2.3 Kubernetes con kind

```bash
kind create cluster --name cells
for s in api web ingestor; do docker build -t cells-$s:local services/$s; done
kind load docker-image cells-api:local cells-web:local cells-ingestor:local --name cells

PGPW=$(openssl rand -hex 16)
kubectl apply -f k8s/00-namespace.yaml
kubectl -n cells create secret generic cells-secrets \
  --from-literal=POSTGRES_PASSWORD=$PGPW \
  --from-literal=DATABASE_URL=postgresql://app:$PGPW@db:5432/cells
kubectl -n cells create configmap db-init --from-file=init.sql=db/init.sql
kubectl apply -f k8s/
kubectl -n cells wait --for=condition=Ready pod --all --timeout=300s
kubectl -n cells port-forward svc/web 8081:80
```

Para cargar los datos y activar el autoescalado, sigue los pasos de la fase 4 de la guía del proyecto. El clúster necesita unos 4 GB de memoria; por eso se usó Codespaces.

## 2.4 Azure con Terraform

```bash
az login --use-device-code
cd infra
cp terraform.tfvars.example terraform.tfvars   # suscripción, región, usuario de GitHub, enlace de OpenCellID
terraform init
terraform plan -out plan.tfplan
terraform apply plan.tfplan
```

`terraform.tfvars` y `terraform.tfstate` contienen secretos y están excluidos en `.gitignore`.

### Ajustes hechos fuera de Terraform

Durante el despliegue real hubo que hacer estos cambios a mano. Deben pasarse a Terraform en la siguiente versión:

| Cambio | Motivo | Comando |
|---|---|---|
| Entorno de Container Apps a `WorkloadProfiles` | Azure lo creó en modo Express, que no admite Jobs |
| Creación de `job-ingestor` | Terraform falló por el modo Express | `az containerapp job create` con disparador `azure-queue` | `az rest --method patch` con `environmentMode: WorkloadProfiles` |
| `allowInsecure` en `ca-api` | La web llega a la API por HTTP interno | `az containerapp ingress update -n ca-api --allow-insecure true` |
| Segunda credencial federada | GitHub usa el formato de sujeto con identificadores numéricos | `az identity federated-credential create --name github-main-v2 ...` |
| Carga inicial de datos | El Job todavía no existía | Ingestor ejecutado desde Codespaces contra PostgreSQL |

## 2.5 CI/CD

| Flujo | Disparador | Qué hace |
|---|---|---|
| `CI` (`.github/workflows/ci.yml`) | Cada *push* y *pull request* | Levanta PostGIS, crea el esquema y ejecuta `pytest` |
| `Deploy` (`.github/workflows/deploy.yml`) | Cada *push* a `main` | Construye y publica las tres imágenes en GHCR; entra a Azure por OIDC y actualiza `ca-web` y `ca-api` |

Secretos y variables del repositorio: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`, `AZURE_RESOURCE_GROUP`, `AZURE_FUNCTION_APP` y `AZURE_READY`.

`Deploy` actualiza `ca-web`, `ca-api` y `job-ingestor`, y publica el código de la Azure Function. El 4 de noviembre de 2026 terminó en verde en todos sus pasos, después de crear `job-ingestor`.
