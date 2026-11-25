# 3. API

API REST en FastAPI. En Azure solo es accesible desde la web, en la ruta `/api`. En local, la documentación interactiva (OpenAPI) está en <http://localhost:8000/docs>.

Todas las respuestas de datos incluyen `attribution`, como exige la licencia CC BY-SA 4.0 de OpenCellID.

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | El proceso está vivo. No consulta la base de datos |
| GET | `/ready` | Lista para recibir tráfico: responde 200 si la base de datos contesta, 503 si no |
| GET | `/v1/cells/nearby?lat&lon&radius_m&limit` | Celdas en un radio (1–20.000 m; hasta 1.000 resultados) |
| GET | `/v1/cells/{radio}/{mcc}/{net}/{area}/{cell}` | Una celda por su identificador completo |
| GET | `/v1/operators?mcc=732` | Número de celdas por red y tecnología |
| POST | `/v1/locate` | Ubicación estimada sin GPS a partir de 1 a 20 celdas detectadas |

## Ejemplos (en Azure, a través de la web)

```bash
WEB=https://ca-web.grayplant-212e438e.northcentralus.azurecontainerapps.io

curl "$WEB/api/v1/cells/nearby?lat=4.65&lon=-74.08&radius_m=2000&limit=5"
curl "$WEB/api/v1/operators"
curl -X POST "$WEB/api/v1/locate" -H "Content-Type: application/json" \
  -d '{"cells":[{"radio":"LTE","mcc":732,"net":101,"area":1000,"cell":5001}]}'
```

Para `locate`, usa los identificadores de una celda que devuelva `nearby`.

## Cómo calcula `locate`

Busca cada celda y hace un promedio ponderado de sus posiciones. Las celdas de menor alcance pesan más, porque ubican con más precisión. `accuracy_m` es el menor alcance entre las celdas usadas. El resultado es siempre una estimación (`"estimated": true`).

## Pruebas

`services/api/tests/test_api.py` contiene 8 pruebas: salud, disponibilidad, búsqueda, celda inexistente, redes, cálculo de `locate`, atribución y validación de entradas. Se ejecutan en cada cambio con GitHub Actions.
