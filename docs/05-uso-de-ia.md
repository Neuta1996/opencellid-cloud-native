# 5. Uso y manejo de la inteligencia artificial

Este proyecto se desarrolló con apoyo de **Claude** (Anthropic), un asistente de IA. Este documento explica cómo lo usamos, cómo lo dirigimos y cómo verificamos lo que produjo.

> Completen o corrijan las partes marcadas con `[equipo]`: deben reflejar lo que hizo cada integrante.

## 5.1 Para qué se usó la IA

| Tarea | Aporte de la IA | Trabajo del equipo |
|---|---|---|
| Entender el reto | Explicar OpenCellID y los requisitos cloud-native | Elegir el caso de negocio y la región |
| Diseño | Proponer la arquitectura y comparar AKS con Container Apps según el crédito | Decidir Container Apps en Azure y Kubernetes en Codespaces |
| Código | Generar la base de la API, la web, el ingestor, Docker, Kubernetes, Terraform y los flujos de CI/CD | Ejecutarlo, probarlo y reportar cada falla |
| Despliegue | Guía paso a paso y comandos | Crear cuentas, ejecutar los comandos y desplegar en Azure |
| Diagnóstico | Interpretar errores a partir de las capturas | Reproducir los errores, enviar evidencia y aplicar las correcciones |
| Pruebas | Diseñar las pruebas de carga y de falla | Ejecutarlas y capturar los resultados |
| Comunicación | Borradores del README, la documentación, el póster, la presentación y los diagramas | Revisarlos, pedir cambios y aprobarlos |

`[equipo]`: indiquen qué integrante hizo cada parte.

## 5.2 Cómo dirigimos la IA

- **Contexto concreto:** le dimos el enunciado, las referencias de la CNCF, la plataforma (OpenCellID) y las restricciones reales: Azure for Students, una sola región permitida (North Central US) y un equipo con poca memoria.
- **Trabajo por fases:** primero local con Docker, luego Kubernetes y al final Azure. Cada fase se validó antes de pasar a la siguiente.
- **Evidencia, no suposiciones:** ante cada error, le enviamos la captura o el registro exacto en lugar de describirlo.
- **Correcciones explícitas:** cuando una respuesta no servía, se lo dijimos y pedimos otra solución; por ejemplo, Codespaces en lugar de Kubernetes local, o íconos estándar en el diagrama.
- **Verificación de cifras:** solo usamos resultados medidos. Cuando no era claro dónde se había ejecutado una prueba de carga, lo revisamos con `history` antes de publicarlo.

## 5.3 Errores de la IA y cómo se corrigieron

| Error o limitación | Efecto | Corrección |
|---|---|---|
| No verificó la memoria del equipo antes de proponer Kubernetes local | El clúster se quedó en `Pending` por falta de memoria | Usar GitHub Codespaces |
| Usó el usuario con mayúsculas en el nombre de las imágenes | Falló el primer `Deploy` | Pasar el registro a minúsculas |
| Recomendó una máquina (B2ats_v2) inadecuada para AKS | Habría fallado en AKS | Corregido en la guía: D2s_v5 solo para demostración |
| No previó que Azure crearía el entorno en modo Express | Azure no permitió crear el Job | Cambiar el entorno a `WorkloadProfiles` y crear el Job con la CLI |
| Documentó la carga diaria como pendiente sin revisar el último `Deploy` | La primera versión de la documentación subestimaba lo desplegado | Revisar los registros de GitHub Actions y corregir el estado |
| La configuración de Nginx usaba HTTP/1.0 | La web recibía error 426 de la API | Agregar `proxy_http_version 1.1` |
| Supuso el formato antiguo del sujeto OIDC | GitHub no pudo entrar a Azure | Registrar el sujeto real que mostró el error |
| El primer diagrama no usaba íconos estándar | Observación del profesor | Diagrama como código con los íconos oficiales de Azure y Kubernetes |
| No advirtió a tiempo el riesgo de costos | El equipo pasó a pago por uso para presentar | Monitorear costos y apagar la base de datos fuera de uso |

## 5.4 Verificación

Lo generado por la IA se consideró correcto solo si pasaba al menos una de estas pruebas:

- **Pruebas automáticas:** 8 pruebas de la API en GitHub Actions.
- **Ejecución real:** Docker, Kubernetes y Azure, con capturas.
- **Mediciones:** k6, Azure Monitor y Log Analytics.
- **Registro de funcionamiento** generado desde la cuenta del equipo.

## 5.5 Responsabilidad

La IA fue una herramienta de apoyo. Las decisiones, la ejecución, la verificación y la entrega son responsabilidad del equipo. No se presentan como propios datos ni resultados que no se hayan medido.
