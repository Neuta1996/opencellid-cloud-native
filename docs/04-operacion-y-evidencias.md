# 4. Accesos, operación y registro de funcionamiento

## 4.1 Accesos

| Recurso | Enlace o acceso |
|---|---|
| Aplicación en Azure | <https://ca-web.grayplant-212e438e.northcentralus.azurecontainerapps.io> |
| Código fuente | <https://github.com/Neuta1996/opencellid-cloud-native> |
| Ejecuciones de CI/CD | <https://github.com/Neuta1996/opencellid-cloud-native/actions> |
| Imágenes de contenedores | <https://github.com/Neuta1996?tab=packages> |
| Portal de Azure | Acceso de lectura (rol **Lector**) al grupo `rg-opencellid`, otorgado al correo del profesor si lo solicita |

La aplicación responde solo cuando la base de datos está encendida. Para ahorrar crédito, se apaga fuera de las revisiones; si el mapa dice «La API no respondió», hay que encenderla.

## 4.2 Operación

```bash
# Encender la base de datos (tarda unos minutos)
az postgres flexible-server start -g rg-opencellid -n psql-cells8mwlpb

# Comprobar que la API está lista
curl https://ca-web.grayplant-212e438e.northcentralus.azurecontainerapps.io/api/ready

# Apagar la base de datos al terminar
az postgres flexible-server stop -g rg-opencellid -n psql-cells8mwlpb
```

Sin tráfico, web y API escalan a cero; la primera visita puede tardar unos segundos en responder.

## 4.3 Registro de funcionamiento

[`registro-funcionamiento.md`](evidencia/registro-funcionamiento.md) es un registro generado con [`scripts/registro-funcionamiento.sh`](../scripts/registro-funcionamiento.sh). Incluye:

1. Recursos desplegados en Azure.
2. Estado de las Container Apps y de la base de datos.
3. Chequeos HTTP con código y tiempo de respuesta.
4. Respuestas reales de la API.
5. Solicitudes por hora en Azure Monitor.
6. Registros de la API en Log Analytics.
7. Eventos de arranque y escalado.
8. Ejecuciones de GitHub Actions.
9. Estado de Kubernetes.

## 4.4 Resultados medidos

| Prueba | Azure | Kubernetes (Codespaces) |
|---|---|---|
| Usuarios simultáneos (k6) | 20 durante 5 min | 20 durante 5 min |
| Solicitudes | 4.536 | 4.747 |
| Errores | 0,00 % | 0,00 % |
| Latencia p95 | 76,37 ms | 43,93 ms |

- **Carga de datos:** 16.214 filas, 0 rechazadas.
- **Resiliencia:** se borró un pod de la API y Kubernetes lo recreó sin intervención.
- **Azure Monitor (`ca-api`, 24 h):** 21,50 ms de respuesta promedio, 1,89 % de CPU, 1 réplica.

## 4.5 Evidencias

| Evidencia | Archivo |
|---|---|
| Mapa en Azure | [mapa-azure.png](evidencia/mapa-azure.png) |
| Mapa en Kubernetes | [mapa-kubernetes.png](evidencia/mapa-kubernetes.png) |
| Mapa local con Docker | [mapa-local-docker.png](evidencia/mapa-local-docker.png) |
| Carga de datos | [carga-datos.png](evidencia/carga-datos.png) |
| Pods de Kubernetes | [pods-kubernetes.png](evidencia/pods-kubernetes.png) |
| Prueba de carga en Azure | [prueba-carga-azure.png](evidencia/prueba-carga-azure.png) |
| Prueba de carga en Kubernetes | [prueba-carga-k6.png](evidencia/prueba-carga-k6.png) |
| GitHub Actions | [github-actions.png](evidencia/github-actions.png) |
| Registro de funcionamiento | [registro-funcionamiento.md](evidencia/registro-funcionamiento.md) |

## 4.6 Costos

Consumo en Azure: **USD 3,70** a inicios de noviembre de 2026, según *Análisis de costos*; casi todo es almacenamiento y red. El mayor costo fijo es PostgreSQL, por eso se apaga cuando no se usa. Al terminar el curso se eliminará el grupo `rg-opencellid`.
