#!/usr/bin/env bash
# Genera docs/evidencia/registro-funcionamiento.md con evidencia real y fechada:
# recursos y estado en Azure, chequeos HTTP, métricas, registros de Log Analytics,
# ejecuciones de GitHub Actions y estado de Kubernetes.
# No imprime contraseñas, cadenas de conexión ni tokens.
#
# Uso (en GitHub Codespaces, con `az login` hecho y la base de datos encendida):
#   bash scripts/registro-funcionamiento.sh
set -u

RG="${RG:-rg-opencellid}"
WEB="${WEB:-https://ca-web.grayplant-212e438e.northcentralus.azurecontainerapps.io}"
OUT="docs/evidencia/registro-funcionamiento.md"
mkdir -p "$(dirname "$OUT")"
az config set extension.use_dynamic_install=yes_without_prompt >/dev/null 2>&1

bloque() {
  local titulo="$1"; shift
  echo
  echo "## $titulo"
  echo
  echo '```text'
  echo "\$ $*"
  "$@" 2>&1 | head -n 60
  echo '```'
}

http() {
  curl -sS -m 60 -o /dev/null -w "$1 -> HTTP %{http_code} en %{time_total} s\n" "$1"
}

WS=$(az monitor log-analytics workspace list -g "$RG" --query "[0].customerId" -o tsv 2>/dev/null)
API_ID=$(az containerapp show -g "$RG" -n ca-api --query id -o tsv 2>/dev/null)
DESDE=$(date -u -d '-24 hours' +%Y-%m-%dT%H:%M:%SZ)

{
  echo "# Registro de funcionamiento"
  echo
  echo "Generado el $(TZ=America/Bogota date '+%Y-%m-%d %H:%M:%S') (hora de Colombia) desde GitHub Codespaces."
  echo
  echo "Aplicación: $WEB"

  bloque "1. Recursos desplegados en Azure" \
    az resource list -g "$RG" --query "[].{Nombre:name, Tipo:type}" -o table
  bloque "2. Estado de las Container Apps" \
    az containerapp list -g "$RG" --query "[].{Nombre:name, Estado:properties.runningStatus, Revision:properties.latestRevisionName}" -o table
  bloque "3. Estado de la base de datos" \
    az postgres flexible-server list -g "$RG" --query "[].{Nombre:name, Estado:state, Version:version, SKU:sku.name}" -o table

  echo
  echo "## 4. Chequeos HTTP de la aplicación"
  echo
  echo '```text'
  http "$WEB/"
  http "$WEB/api/health"
  http "$WEB/api/ready"
  echo
  echo "\$ curl $WEB/api/ready"
  curl -sS -m 60 "$WEB/api/ready"; echo
  echo
  echo "\$ curl \"$WEB/api/v1/cells/nearby?lat=4.65&lon=-74.08&radius_m=2000&limit=3\""
  curl -sS -m 60 "$WEB/api/v1/cells/nearby?lat=4.65&lon=-74.08&radius_m=2000&limit=3" | python3 -m json.tool | head -n 40
  echo
  echo "\$ curl $WEB/api/v1/operators"
  curl -sS -m 60 "$WEB/api/v1/operators" | python3 -m json.tool | head -n 40
  echo '```'

  if [ -n "$API_ID" ]; then
    bloque "5. Métricas de Azure Monitor (ca-api, últimas 24 h, por hora)" \
      az monitor metrics list --resource "$API_ID" --metric Requests --aggregation Total \
        --interval PT1H --start-time "$DESDE" \
        --query "value[0].timeseries[0].data[?total > \`0\`].{Hora:timeStamp, Solicitudes:total}" -o table
  fi

  if [ -n "$WS" ]; then
    bloque "6. Registros de la API en Log Analytics (últimos 20)" \
      az monitor log-analytics query -w "$WS" -o table --analytics-query \
        "ContainerAppConsoleLogs_CL | where ContainerAppName_s == 'ca-api' | where TimeGenerated > ago(7d) | top 20 by TimeGenerated desc | project TimeGenerated, Log_s"
    bloque "7. Eventos del sistema: arranques y escalado (últimos 20)" \
      az monitor log-analytics query -w "$WS" -o table --analytics-query \
        "ContainerAppSystemLogs_CL | where TimeGenerated > ago(7d) | top 20 by TimeGenerated desc | project TimeGenerated, ContainerAppName_s, Reason_s"
  fi

  bloque "8a. Ejecuciones de job-ingestor (carga diaria disparada por la cola)" \
    az containerapp job execution list -g "$RG" -n job-ingestor \
      --query "[].{Inicio:properties.startTime, Fin:properties.endTime, Estado:properties.status}" -o table
  if [ -n "$WS" ]; then
    bloque "8b. Ejecuciones de la Azure Function (Application Insights)" \
      az monitor log-analytics query -w "$WS" -o table --analytics-query \
        "AppRequests | where TimeGenerated > ago(30d) | where Name has 'daily_download' | top 20 by TimeGenerated desc | project TimeGenerated, Name, Success, DurationMs"
    bloque "8c. Mensajes del ingestor (filas cargadas)" \
      az monitor log-analytics query -w "$WS" -o table --analytics-query \
        "ContainerAppConsoleLogs_CL | where column_ifexists('ContainerJobName_s', '') == 'job-ingestor' or ContainerAppName_s == 'job-ingestor' | where Log_s has 'cargadas' or Log_s has 'mensajes' or Log_s has 'ERROR' | top 20 by TimeGenerated desc | project TimeGenerated, Log_s"
  fi
  bloque "8d. Archivos descargados en Blob Storage" \
    az storage blob list --account-name stcells8mwlpb --container-name raw --auth-mode key \
      --query "[].{Archivo:name, Fecha:properties.lastModified, Bytes:properties.contentLength}" -o table

  if command -v gh >/dev/null 2>&1; then
    bloque "9. Ejecuciones de GitHub Actions" gh run list --limit 15
  fi

  if command -v kubectl >/dev/null 2>&1 && kubectl -n cells get pods >/dev/null 2>&1; then
    bloque "10. Kubernetes en Codespaces" kubectl -n cells get pods,svc,hpa
  else
    echo
    echo "## 10. Kubernetes en Codespaces"
    echo
    echo "El clúster no estaba activo al generar este registro. Ver docs/evidencia/pods-kubernetes.png."
  fi
} > "$OUT"

echo "Registro guardado en $OUT"
