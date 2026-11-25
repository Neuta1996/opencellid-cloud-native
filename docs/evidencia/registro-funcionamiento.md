# Registro de funcionamiento

Generado el 2026-11-24 22:01:02 (hora de Colombia) desde GitHub Codespaces.

Aplicación: https://ca-web.grayplant-212e438e.northcentralus.azurecontainerapps.io

## 1. Recursos desplegados en Azure

```text
$ az resource list -g rg-opencellid --query [].{Nombre:name, Tipo:type} -o table
Nombre                                Tipo
------------------------------------  ------------------------------------------------
asp-cells8mwlpb                       Microsoft.Web/serverFarms
psql-cells8mwlpb                      Microsoft.DBforPostgreSQL/flexibleServers
log-cells8mwlpb                       Microsoft.OperationalInsights/workspaces
stcells8mwlpb                         Microsoft.Storage/storageAccounts
appi-cells8mwlpb                      Microsoft.Insights/components
cae-cells8mwlpb                       Microsoft.App/managedEnvironments
func-cells8mwlpb                      Microsoft.Web/sites
ca-api                                Microsoft.App/containerApps
ca-web                                Microsoft.App/containerApps
Application Insights Smart Detection  microsoft.insights/actiongroups
id-github                             Microsoft.ManagedIdentity/userAssignedIdentities
job-ingestor                          Microsoft.App/jobs
```

## 2. Estado de las Container Apps

```text
$ az containerapp list -g rg-opencellid --query [].{Nombre:name, Estado:properties.runningStatus, Revision:properties.latestRevisionName} -o table
Nombre    Estado    Revision
--------  --------  ---------------
ca-api    Running   ca-api--0000004
ca-web    Running   ca-web--0000004
```

## 3. Estado de la base de datos

```text
$ az postgres flexible-server list -g rg-opencellid --query [].{Nombre:name, Estado:state, Version:version, SKU:sku.name} -o table
Nombre            Estado    Version    SKU
----------------  --------  ---------  -------------
psql-cells8mwlpb  Ready     16         Standard_B1ms
```

## 4. Chequeos HTTP de la aplicación

```text
https://ca-web.grayplant-212e438e.northcentralus.azurecontainerapps.io/ -> HTTP 200 en 0.097981 s
https://ca-web.grayplant-212e438e.northcentralus.azurecontainerapps.io/api/health -> HTTP 200 en 0.102242 s
https://ca-web.grayplant-212e438e.northcentralus.azurecontainerapps.io/api/ready -> HTTP 200 en 0.084211 s

$ curl https://ca-web.grayplant-212e438e.northcentralus.azurecontainerapps.io/api/ready
{"status":"ready"}

$ curl "https://ca-web.grayplant-212e438e.northcentralus.azurecontainerapps.io/api/v1/cells/nearby?lat=4.65&lon=-74.08&radius_m=2000&limit=3"
{
    "count": 3,
    "cells": [
        {
            "radio": "GSM",
            "mcc": 732,
            "net": 101,
            "area": 5027,
            "cell": 62754,
            "lon": -74.0938,
            "lat": 4.6404,
            "range_m": 1000,
            "samples": 1,
            "updated_at": "2025-05-20T11:20:06+00:00"
        },
        {
            "radio": "GSM",
            "mcc": 732,
            "net": 123,
            "area": 2132,
            "cell": 21032,
            "lon": -74.0768,
            "lat": 4.6554,
            "range_m": 3166,
            "samples": 24,
            "updated_at": "2025-05-10T05:46:43+00:00"
        },
        {
            "radio": "LTE",
            "mcc": 732,
            "net": 101,
            "area": 67,
            "cell": 55541,
            "lon": -74.0917,
            "lat": 4.6511,
            "range_m": 1000,
            "samples": 1,
            "updated_at": "2025-05-08T21:58:40+00:00"
        }
    ],

$ curl https://ca-web.grayplant-212e438e.northcentralus.azurecontainerapps.io/api/v1/operators
{
    "mcc": 732,
    "operators": [
        {
            "net": 2,
            "radio": "LTE",
            "cells": 1
        },
        {
            "net": 2,
            "radio": "UMTS",
            "cells": 20
        },
        {
            "net": 101,
            "radio": "GSM",
            "cells": 2367
        },
        {
            "net": 101,
            "radio": "LTE",
            "cells": 1337
        },
        {
            "net": 101,
            "radio": "UMTS",
            "cells": 4726
        },
        {
            "net": 103,
            "radio": "GSM",
            "cells": 30
        },
        {
            "net": 103,
            "radio": "LTE",
            "cells": 833
        },
        {
            "net": 103,
```

## 5. Métricas de Azure Monitor (ca-api, últimas 24 h, por hora)

```text
$ az monitor metrics list --resource /subscriptions/8666d529-81e4-4761-a826-02865edb0d91/resourceGroups/rg-opencellid/providers/Microsoft.App/containerapps/ca-api --metric Requests --aggregation Total --interval PT1H --start-time 2026-11-24T03:01:02Z --query value[0].timeseries[0].data[?total > `0`].{Hora:timeStamp, Solicitudes:total} -o table

```

## 6. Registros de la API en Log Analytics (últimos 20)

```text
$ az monitor log-analytics query -w cd258934-cac1-4b2d-8ba3-b8d97030a88b -o table --analytics-query ContainerAppConsoleLogs_CL | where ContainerAppName_s == 'ca-api' | where TimeGenerated > ago(7d) | top 20 by TimeGenerated desc | project TimeGenerated, Log_s
WARNING: Preview version of extension is disabled by default for extension installation, enabled for modules without stable versions. 
WARNING: Please run 'az config set extension.dynamic_install_allow_preview=true or false' to config it specifically. 
WARNING: The command requires the extension log-analytics. It will be installed first.
WARNING: No stable version of 'log-analytics' to install. Preview versions allowed.
WARNING: The installed extension 'log-analytics' is in preview.
Log_s                                                                                                            TableName      TimeGenerated
---------------------------------------------------------------------------------------------------------------  -------------  ----------------------------
INFO:     127.0.0.1:54732 - "GET /ready HTTP/1.1" 200 OK                                                         PrimaryResult  2026-11-25T03:01:16.7831497Z
INFO:     100.100.0.40:44652 - "GET /v1/operators HTTP/1.1" 200 OK                                               PrimaryResult  2026-11-25T03:01:07.7749624Z
INFO:     127.0.0.1:59828 - "GET /health HTTP/1.1" 200 OK                                                        PrimaryResult  2026-11-25T03:01:07.7749624Z
INFO:     100.100.0.112:54746 - "GET /ready HTTP/1.1" 200 OK                                                     PrimaryResult  2026-11-25T03:01:07.7749624Z
INFO:     100.100.0.40:44650 - "GET /ready HTTP/1.1" 200 OK                                                      PrimaryResult  2026-11-25T03:01:07.7749624Z
INFO:     100.100.0.40:44652 - "GET /v1/cells/nearby?lat=4.65&lon=-74.08&radius_m=2000&limit=3 HTTP/1.1" 200 OK  PrimaryResult  2026-11-25T03:01:07.7749624Z
INFO:     100.100.0.40:44650 - "GET /health HTTP/1.1" 200 OK                                                     PrimaryResult  2026-11-25T03:01:07.7749624Z
INFO:     127.0.0.1:59820 - "GET /ready HTTP/1.1" 200 OK                                                         PrimaryResult  2026-11-25T03:01:07.0001672Z
INFO:     127.0.0.1:36800 - "GET /health HTTP/1.1" 200 OK                                                        PrimaryResult  2026-11-25T03:00:57.9452018Z
INFO:     127.0.0.1:36794 - "GET /ready HTTP/1.1" 200 OK                                                         PrimaryResult  2026-11-25T03:00:56.9376497Z
INFO:     127.0.0.1:36600 - "GET /health HTTP/1.1" 200 OK                                                        PrimaryResult  2026-11-25T03:00:47.8198689Z
INFO:     127.0.0.1:36592 - "GET /ready HTTP/1.1" 200 OK                                                         PrimaryResult  2026-11-25T03:00:46.7127009Z
INFO:     127.0.0.1:40948 - "GET /health HTTP/1.1" 200 OK                                                        PrimaryResult  2026-11-25T03:00:37.8648668Z
INFO:     127.0.0.1:40938 - "GET /ready HTTP/1.1" 200 OK                                                         PrimaryResult  2026-11-25T03:00:36.8786804Z
INFO:     127.0.0.1:34148 - "GET /health HTTP/1.1" 200 OK                                                        PrimaryResult  2026-11-25T03:00:27.833884Z
INFO:     127.0.0.1:34142 - "GET /ready HTTP/1.1" 200 OK                                                         PrimaryResult  2026-11-25T03:00:26.6945618Z
INFO:     127.0.0.1:47808 - "GET /health HTTP/1.1" 200 OK                                                        PrimaryResult  2026-11-25T03:00:17.7603947Z
INFO:     127.0.0.1:47804 - "GET /ready HTTP/1.1" 200 OK                                                         PrimaryResult  2026-11-25T03:00:16.6735229Z
INFO:     127.0.0.1:49818 - "GET /health HTTP/1.1" 200 OK                                                        PrimaryResult  2026-11-25T03:00:08.0089712Z
INFO:     127.0.0.1:49812 - "GET /ready HTTP/1.1" 200 OK                                                         PrimaryResult  2026-11-25T03:00:06.898161Z
```

## 7. Eventos del sistema: arranques y escalado (últimos 20)

```text
$ az monitor log-analytics query -w cd258934-cac1-4b2d-8ba3-b8d97030a88b -o table --analytics-query ContainerAppSystemLogs_CL | where TimeGenerated > ago(7d) | top 20 by TimeGenerated desc | project TimeGenerated, ContainerAppName_s, Reason_s
ContainerAppName_s    Reason_s                  TableName      TimeGenerated
--------------------  ------------------------  -------------  ----------------------------
                      Completed                 PrimaryResult  2026-11-25T03:01:01.1743798Z
                      ContainerTerminated       PrimaryResult  2026-11-25T03:00:56.066241Z
                      ContainerStarted          PrimaryResult  2026-11-25T03:00:54.1012488Z
                      ContainerCreated          PrimaryResult  2026-11-25T03:00:54.1012488Z
                      PulledImage               PrimaryResult  2026-11-25T03:00:53.2279909Z
                      AssigningReplica          PrimaryResult  2026-11-25T03:00:34.1214618Z
                      SuccessfulCreate          PrimaryResult  2026-11-25T03:00:34.1214618Z
                      ScaledJobActive           PrimaryResult  2026-11-25T03:00:33.1148746Z
                      KEDAJobsCreated           PrimaryResult  2026-11-25T03:00:33.1148746Z
                      KEDAJobMetricActive       PrimaryResult  2026-11-25T03:00:33.1148746Z
                      KEDAJobAggregatedMetrics  PrimaryResult  2026-11-25T02:58:33.1232682Z
                      KEDAScalingDecision       PrimaryResult  2026-11-25T02:58:33.1232682Z
                      KEDAJobMetricInactive     PrimaryResult  2026-11-25T02:58:33.1232682Z
                      KEDAJobMetricInactive     PrimaryResult  2026-11-25T02:57:33.4110768Z
                      KEDAJobAggregatedMetrics  PrimaryResult  2026-11-25T02:57:33.4110768Z
                      KEDAScalingDecision       PrimaryResult  2026-11-25T02:57:33.4110768Z
ca-api                KEDAScalersStopped        PrimaryResult  2026-11-25T02:56:50.089972Z
ca-api                ScaledObjectDeleted       PrimaryResult  2026-11-25T02:56:50.089972Z
                      KEDAScalingDecision       PrimaryResult  2026-11-25T02:56:33.3579059Z
                      KEDAJobAggregatedMetrics  PrimaryResult  2026-11-25T02:56:33.3579059Z
```

## 8a. Ejecuciones de job-ingestor (carga diaria disparada por la cola)

```text
$ az containerapp job execution list -g rg-opencellid -n job-ingestor --query [].{Inicio:properties.startTime, Fin:properties.endTime, Estado:properties.status} -o table
Inicio                     Fin                        Estado
-------------------------  -------------------------  ---------
2026-11-25T03:00:32+00:00  2026-11-25T03:01:00+00:00  Succeeded
2026-11-24T03:00:11+00:00  2026-11-24T03:00:45+00:00  Succeeded
2026-11-23T03:00:10+00:00  2026-11-23T03:00:38+00:00  Succeeded
2026-11-22T03:00:10+00:00  2026-11-22T03:00:41+00:00  Succeeded
2026-11-21T03:00:09+00:00  2026-11-21T03:00:34+00:00  Succeeded
2026-11-20T03:00:08+00:00  2026-11-20T03:01:01+00:00  Succeeded
2026-11-19T04:32:07+00:00  2026-11-19T04:32:40+00:00  Succeeded
2026-11-19T04:31:07+00:00  2026-11-19T04:31:34+00:00  Succeeded
2026-11-19T04:30:07+00:00  2026-11-19T04:30:34+00:00  Succeeded
2026-11-19T04:29:07+00:00  2026-11-19T04:29:34+00:00  Succeeded
2026-11-19T04:28:07+00:00  2026-11-19T04:28:29+00:00  Succeeded
2026-11-19T04:27:07+00:00  2026-11-19T04:27:33+00:00  Succeeded
2026-11-19T04:26:07+00:00  2026-11-19T04:26:28+00:00  Succeeded
2026-11-19T04:25:07+00:00  2026-11-19T04:25:38+00:00  Succeeded
2026-11-19T04:24:07+00:00  2026-11-19T04:24:38+00:00  Succeeded
2026-11-19T04:23:07+00:00  2026-11-19T04:23:37+00:00  Succeeded
2026-11-19T04:22:07+00:00  2026-11-19T04:22:37+00:00  Succeeded
2026-11-19T04:21:07+00:00  2026-11-19T04:21:37+00:00  Succeeded
2026-11-19T04:20:07+00:00  2026-11-19T04:20:27+00:00  Succeeded
2026-11-19T04:19:07+00:00  2026-11-19T04:19:36+00:00  Succeeded
2026-11-19T04:18:07+00:00  2026-11-19T04:18:36+00:00  Succeeded
2026-11-19T04:17:07+00:00  2026-11-19T04:17:36+00:00  Succeeded
2026-11-19T04:16:07+00:00  2026-11-19T04:16:41+00:00  Succeeded
2026-11-19T04:15:07+00:00  2026-11-19T04:15:35+00:00  Succeeded
2026-11-19T04:14:07+00:00  2026-11-19T04:14:35+00:00  Succeeded
2026-11-19T04:13:07+00:00  2026-11-19T04:13:35+00:00  Succeeded
2026-11-19T04:12:07+00:00  2026-11-19T04:12:39+00:00  Succeeded
2026-11-19T04:11:07+00:00  2026-11-19T04:11:39+00:00  Succeeded
2026-11-19T04:10:07+00:00  2026-11-19T04:10:34+00:00  Succeeded
2026-11-19T04:09:07+00:00  2026-11-19T04:09:34+00:00  Succeeded
2026-11-19T04:08:07+00:00  2026-11-19T04:08:33+00:00  Succeeded
2026-11-19T04:07:07+00:00  2026-11-19T04:07:33+00:00  Succeeded
2026-11-19T04:06:07+00:00  2026-11-19T04:06:38+00:00  Succeeded
2026-11-19T04:02:07+00:00  2026-11-19T04:05:13+00:00  Succeeded
2026-11-19T04:01:07+00:00  2026-11-19T04:01:37+00:00  Succeeded
2026-11-19T04:00:07+00:00  2026-11-19T04:00:36+00:00  Succeeded
2026-11-19T03:59:07+00:00  2026-11-19T03:59:36+00:00  Succeeded
2026-11-19T03:58:07+00:00  2026-11-19T03:58:36+00:00  Succeeded
2026-11-19T03:57:07+00:00  2026-11-19T03:57:36+00:00  Succeeded
2026-11-19T03:56:07+00:00  2026-11-19T03:56:40+00:00  Succeeded
2026-11-19T03:55:07+00:00  2026-11-19T03:55:40+00:00  Succeeded
2026-11-19T03:54:07+00:00  2026-11-19T03:54:40+00:00  Succeeded
2026-11-19T03:53:07+00:00  2026-11-19T03:53:34+00:00  Succeeded
2026-11-19T03:52:07+00:00  2026-11-19T03:52:34+00:00  Succeeded
2026-11-19T03:51:07+00:00  2026-11-19T03:51:34+00:00  Succeeded
2026-11-19T03:50:07+00:00  2026-11-19T03:50:34+00:00  Succeeded
2026-11-19T03:49:07+00:00  2026-11-19T03:49:33+00:00  Succeeded
2026-11-19T03:48:07+00:00  2026-11-19T03:48:38+00:00  Succeeded
2026-11-19T03:47:07+00:00  2026-11-19T03:47:38+00:00  Succeeded
2026-11-19T03:46:07+00:00  2026-11-19T03:46:37+00:00  Succeeded
2026-11-19T03:45:07+00:00  2026-11-19T03:45:37+00:00  Succeeded
2026-11-19T03:44:07+00:00  2026-11-19T03:44:37+00:00  Succeeded
2026-11-19T03:43:07+00:00  2026-11-19T03:43:37+00:00  Succeeded
2026-11-19T03:42:07+00:00  2026-11-19T03:42:36+00:00  Succeeded
2026-11-19T03:41:07+00:00  2026-11-19T03:41:36+00:00  Succeeded
2026-11-19T03:40:07+00:00  2026-11-19T03:40:36+00:00  Succeeded
2026-11-19T03:39:07+00:00  2026-11-19T03:39:41+00:00  Succeeded
2026-11-19T03:38:07+00:00  2026-11-19T03:38:35+00:00  Succeeded
```

## 8b. Ejecuciones de la Azure Function (Application Insights)

```text
$ az monitor log-analytics query -w cd258934-cac1-4b2d-8ba3-b8d97030a88b -o table --analytics-query AppRequests | where TimeGenerated > ago(30d) | where Name has 'daily_download' | top 20 by TimeGenerated desc | project TimeGenerated, Name, Success, DurationMs
DurationMs    Name            Success    TableName      TimeGenerated
------------  --------------  ---------  -------------  ----------------------------
1047.822      daily_download  True       PrimaryResult  2026-11-25T03:00:00.0045139Z
918.7035      daily_download  True       PrimaryResult  2026-11-24T03:00:00.006612Z
920.1033      daily_download  True       PrimaryResult  2026-11-23T03:00:00.0071254Z
963.3362      daily_download  True       PrimaryResult  2026-11-22T03:00:00.0187312Z
974.3898      daily_download  True       PrimaryResult  2026-11-21T03:00:00.0048097Z
918.0979      daily_download  True       PrimaryResult  2026-11-20T03:00:00.0023832Z
1032.8072     daily_download  True       PrimaryResult  2026-11-19T03:00:00.0067158Z
904.2698      daily_download  True       PrimaryResult  2026-11-18T03:00:00.0053873Z
901.0667      daily_download  True       PrimaryResult  2026-11-17T03:00:00.0086399Z
920.7867      daily_download  True       PrimaryResult  2026-11-16T03:00:00.0024575Z
894.2817      daily_download  True       PrimaryResult  2026-11-15T03:00:00.0019558Z
970.4047      daily_download  True       PrimaryResult  2026-11-14T03:00:00.0100692Z
938.077       daily_download  True       PrimaryResult  2026-11-13T03:00:00.0182241Z
886.1823      daily_download  True       PrimaryResult  2026-11-12T03:00:00.0049721Z
1049.6753     daily_download  True       PrimaryResult  2026-11-11T03:00:00.0074544Z
1000.1396     daily_download  True       PrimaryResult  2026-11-10T03:00:00.0129425Z
930.8569      daily_download  True       PrimaryResult  2026-11-09T03:00:00.0033052Z
1099.1415     daily_download  True       PrimaryResult  2026-11-08T03:00:00.0079127Z
1283.85       daily_download  True       PrimaryResult  2026-11-07T03:00:00.0036163Z
1062.3361     daily_download  True       PrimaryResult  2026-11-06T03:00:00.0109026Z
```

## 8c. Mensajes del ingestor (filas cargadas)

```text
$ az monitor log-analytics query -w cd258934-cac1-4b2d-8ba3-b8d97030a88b -o table --analytics-query ContainerAppConsoleLogs_CL | where column_ifexists('ContainerJobName_s', '') == 'job-ingestor' or ContainerAppName_s == 'job-ingestor' | where Log_s has 'cargadas' or Log_s has 'mensajes' or Log_s has 'ERROR' | top 20 by TimeGenerated desc | project TimeGenerated, Log_s
Log_s                                                                        TableName      TimeGenerated
---------------------------------------------------------------------------  -------------  ----------------------------
INFO cargadas=16367 rechazadas=0                                             PrimaryResult  2026-11-25T03:00:55.5173226Z
INFO cargadas=16382 rechazadas=0                                             PrimaryResult  2026-11-24T03:00:39.0476074Z
INFO cargadas=16405 rechazadas=0                                             PrimaryResult  2026-11-23T03:00:35.0202352Z
INFO cargadas=16400 rechazadas=0                                             PrimaryResult  2026-11-22T03:00:34.098611Z
INFO cargadas=16414 rechazadas=0                                             PrimaryResult  2026-11-21T03:00:30.0030115Z
INFO cargadas=16388 rechazadas=0                                             PrimaryResult  2026-11-20T03:00:55.4254771Z
ERROR Mensaje descartado tras 3 intentos: {"blob": "2026-11-19/732.csv.gz"}  PrimaryResult  2026-11-19T04:32:37.2004731Z
INFO No hay mensajes en la cola                                              PrimaryResult  2026-11-19T04:31:30.119558Z
INFO No hay mensajes en la cola                                              PrimaryResult  2026-11-19T04:30:27.1615836Z
INFO No hay mensajes en la cola                                              PrimaryResult  2026-11-19T04:29:29.6896902Z
INFO No hay mensajes en la cola                                              PrimaryResult  2026-11-19T04:28:20.9494883Z
INFO No hay mensajes en la cola                                              PrimaryResult  2026-11-19T04:27:29.4446431Z
INFO No hay mensajes en la cola                                              PrimaryResult  2026-11-19T04:26:20.2637637Z
INFO No hay mensajes en la cola                                              PrimaryResult  2026-11-19T04:25:30.8984664Z
INFO No hay mensajes en la cola                                              PrimaryResult  2026-11-19T04:24:30.1867086Z
INFO No hay mensajes en la cola                                              PrimaryResult  2026-11-19T04:23:28.7018052Z
INFO No hay mensajes en la cola                                              PrimaryResult  2026-11-19T04:22:29.4982431Z
INFO No hay mensajes en la cola                                              PrimaryResult  2026-11-19T04:21:29.289815Z
INFO No hay mensajes en la cola                                              PrimaryResult  2026-11-19T04:20:21.2384225Z
INFO No hay mensajes en la cola                                              PrimaryResult  2026-11-19T04:19:30.8692963Z
```

## 8d. Archivos descargados en Blob Storage

```text
$ az storage blob list --account-name stcells8mwlpb --container-name raw --auth-mode key --query [].{Archivo:name, Fecha:properties.lastModified, Bytes:properties.contentLength} -o table
WARNING: 
There are no credentials provided in your command and environment, we will query for account key for your storage account.
It is recommended to provide --connection-string, --account-key or --sas-token in your command as credentials.

You also can add `--auth-mode login` in your command to use Azure Active Directory (Azure AD) for authorization if your login account is assigned required RBAC roles.
For more information about RBAC roles in storage, visit https://learn.microsoft.com/azure/storage/common/storage-auth-aad-rbac-cli.

In addition, setting the corresponding environment variables can avoid inputting credentials in your command. Please use --help to get more information about environment variable usage.
Archivo                Fecha                      Bytes
---------------------  -------------------------  -------
2026-11-05/732.csv.gz  2026-11-05T03:00:00+00:00  325019
2026-11-06/732.csv.gz  2026-11-06T03:00:01+00:00  325127
2026-11-07/732.csv.gz  2026-11-07T03:00:01+00:00  325266
2026-11-08/732.csv.gz  2026-11-08T03:00:01+00:00  325135
2026-11-09/732.csv.gz  2026-11-09T03:00:00+00:00  327310
2026-11-10/732.csv.gz  2026-11-10T03:00:00+00:00  326832
2026-11-11/732.csv.gz  2026-11-11T03:00:01+00:00  325876
2026-11-12/732.csv.gz  2026-11-12T03:00:00+00:00  325262
2026-11-13/732.csv.gz  2026-11-13T03:00:00+00:00  325141
2026-11-14/732.csv.gz  2026-11-14T03:00:00+00:00  325140
2026-11-15/732.csv.gz  2026-11-15T03:00:00+00:00  324920
2026-11-16/732.csv.gz  2026-11-16T03:00:00+00:00  325250
2026-11-17/732.csv.gz  2026-11-17T03:00:00+00:00  325317
2026-11-18/732.csv.gz  2026-11-18T03:00:00+00:00  327004
2026-11-19/732.csv.gz  2026-11-19T03:00:00+00:00  327168
2026-11-20/732.csv.gz  2026-11-20T03:00:00+00:00  327737
2026-11-21/732.csv.gz  2026-11-21T03:00:00+00:00  328232
2026-11-22/732.csv.gz  2026-11-22T03:00:00+00:00  327822
2026-11-23/732.csv.gz  2026-11-23T03:00:00+00:00  327859
2026-11-24/732.csv.gz  2026-11-24T03:00:00+00:00  327388
2026-11-25/732.csv.gz  2026-11-25T03:00:00+00:00  327052
```

## 9. Ejecuciones de GitHub Actions

```text
$ gh run list --limit 15
completed	success	Corregir estado de la carga diaria y registrar sus ejecuciones	CI	main	push	45536191373	30s	2026-11-25T02:54:01Z
completed	success	Corregir estado de la carga diaria y registrar sus ejecuciones	Deploy	main	push	45536191306	2m11s	2026-11-25T02:54:01Z
completed	success	Segunda entrega: documentación, arquitectura con íconos estándar, reg…	Deploy	main	push	45536083591	2m5s	2026-11-25T02:53:04Z
completed	success	Segunda entrega: documentación, arquitectura con íconos estándar, reg…	CI	main	push	45536083579	34s	2026-11-25T02:53:04Z
completed	success	Actualizar README, resultados y evidencias	Deploy	main	push	41779932824	2m14s	2026-11-04T05:33:05Z
completed	success	Actualizar README, resultados y evidencias	CI	main	push	41779932688	32s	2026-11-04T05:33:05Z
completed	success	Usar HTTP 1.1 entre la web y la API	Deploy	main	push	41776557764	2m8s	2026-11-04T05:00:21Z
completed	success	Usar HTTP 1.1 entre la web y la API	CI	main	push	41776557462	42s	2026-11-04T05:00:21Z
completed	success	Deploy	Deploy	main	workflow_dispatch	41775791609	2m7s	2026-11-04T04:52:21Z
completed	failure	Deploy	Deploy	main	workflow_dispatch	41774046205	48s	2026-11-04T04:34:42Z
completed	failure	Deploy	Deploy	main	workflow_dispatch	41771825937	1m43s	2026-11-04T04:12:54Z
completed	failure	Deploy	Deploy	main	workflow_dispatch	41771456598	48s	2026-11-04T04:09:19Z
completed	success	Corregir carga del mapa	CI	main	push	41767441232	30s	2026-11-04T03:29:31Z
completed	success	Corregir carga del mapa	Deploy	main	push	41767441218	51s	2026-11-04T03:29:31Z
completed	success	Usar minusculas en el registro de imagenes	Deploy	main	push	41747759140	33s	2026-11-04T00:33:50Z
```

## 10. Kubernetes en Codespaces

El clúster no estaba activo al generar este registro. Ver docs/evidencia/pods-kubernetes.png.
