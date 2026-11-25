"""Diagrama de arquitectura como código, con los íconos oficiales de Azure y Kubernetes.

Requisitos: Graphviz y `pip install diagrams`.
Uso: python docs/diagrama/diagrama.py
Genera docs/arquitectura.png (Azure y DevOps) y docs/arquitectura-kubernetes.png.
"""
from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.azure.compute import ContainerApps, FunctionApps
from diagrams.azure.database import DatabaseForPostgresqlServers
from diagrams.azure.identity import ManagedIdentities
from diagrams.azure.monitor import LogAnalyticsWorkspaces, Metrics
from diagrams.azure.storage import BlobStorage, QueuesStorage
from diagrams.k8s.clusterconfig import HPA
from diagrams.k8s.compute import Deploy, STS
from diagrams.k8s.network import SVC
from diagrams.k8s.podconfig import Secret
from diagrams.k8s.storage import PVC
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.client import Users
from diagrams.onprem.container import Docker
from diagrams.onprem.iac import Terraform
from diagrams.onprem.network import Internet
from diagrams.onprem.vcs import Github

DOCS = Path(__file__).resolve().parent.parent

EVENTOS = dict(color="#C57A00")
DATOS = dict(color="#2F8F5B")
DEVOPS = dict(color="#3A1FB0")

grafo = {
    "fontsize": "22", "fontname": "Helvetica-Bold", "labelloc": "t",
    "pad": "0.4", "nodesep": "0.7", "ranksep": "1.1", "dpi": "160",
    "bgcolor": "white", "splines": "spline",
}
nodo = {"fontsize": "13", "fontname": "Helvetica"}
borde = {"fontsize": "12", "fontname": "Helvetica"}

with Diagram(
    "Plataforma cloud-native con OpenCellID: arquitectura en Azure (verde: consultas · naranja: carga diaria · morado: DevOps)",
    filename=str(DOCS / "arquitectura"), outformat="png", show=False, direction="LR",
    graph_attr=grafo, node_attr=nodo, edge_attr=borde,
):
    usuarios = Users("Usuarios\n(navegador)")
    opencellid = Internet("OpenCellID\nCSV Colombia (MCC 732)")

    with Cluster("GitHub · DevOps y CI/CD"):
        repo = Github("Repositorio\nopencellid-cloud-native")
        ci = GithubActions("Actions\nCI (pytest + PostGIS)\nDeploy")
        ghcr = Docker("GHCR\ncells-web · cells-api\ncells-ingestor")
        repo >> Edge(**DEVOPS) >> ci >> Edge(label="build y push", **DEVOPS) >> ghcr

    iac = Terraform("Terraform\n(infraestructura\ncomo código)")

    with Cluster("Microsoft Azure · Azure for Students · North Central US · rg-opencellid"):
        identidad = ManagedIdentities("id-github\n(OIDC federado)")

        with Cluster("Container Apps Environment · cae-cells8mwlpb"):
            web = ContainerApps("ca-web\nNginx + Leaflet\npúblico HTTPS · 0–2")
            api = ContainerApps("ca-api\nFastAPI · interno\n0–3 réplicas")
            job = ContainerApps("job-ingestor\nContainer Apps Job\n(KEDA, cola)")

        db = DatabaseForPostgresqlServers("PostgreSQL Flexible\nB1ms + PostGIS\nunas 16.400 celdas\nactualizadas a diario")

        with Cluster("Carga diaria orientada a eventos"):
            funcion = FunctionApps("Azure Function\ntemporizador\n22:00 Colombia")
            blob = BlobStorage("Blob · raw")
            cola = QueuesStorage("Queue · ingest-jobs")

        with Cluster("Observabilidad"):
            logs = LogAnalyticsWorkspaces("Log Analytics")
            metricas = Metrics("Azure Monitor\nmétricas")

    # Uso de la aplicación
    usuarios >> Edge(label="HTTPS", **DATOS) >> web
    web >> Edge(label="/api · HTTP/1.1", **DATOS) >> api
    api >> Edge(label="consultas PostGIS · TLS", **DATOS) >> db

    # Carga de datos
    opencellid >> Edge(label="descarga diaria", **EVENTOS) >> funcion
    funcion >> Edge(**EVENTOS) >> blob
    funcion >> Edge(label="aviso", **EVENTOS) >> cola
    cola >> Edge(label="dispara", **EVENTOS) >> job
    job >> Edge(label="carga", **EVENTOS) >> db

    # Despliegue
    ci >> Edge(label="login OIDC", **DEVOPS) >> identidad
    identidad >> Edge(label="actualiza imágenes", **DEVOPS) >> web
    ghcr >> Edge(label="imágenes", style="dotted") >> api
    iac >> Edge(label="crea recursos", **DEVOPS) >> db

    # Monitoreo
    api >> Edge(style="dotted", color="#7A6FD0") >> logs
    web >> Edge(style="dotted", color="#7A6FD0") >> metricas


with Diagram(
    "Kubernetes (kind en GitHub Codespaces): mismas imágenes, réplicas, autoescalado y resiliencia",
    filename=str(DOCS / "arquitectura-kubernetes"), outformat="png", show=False, direction="LR",
    graph_attr=grafo, node_attr=nodo, edge_attr=borde,
):
    ghcr_k = Docker("GHCR\nimágenes de\nlos servicios")
    usuario_k = Users("Usuario\n(port-forward 8081)")
    with Cluster("Kubernetes (kind en GitHub Codespaces) · portabilidad"):
        k_svc = SVC("Service web")
        k_web = Deploy("Deployment web\n2 réplicas")
        k_api = Deploy("Deployment api\n2 réplicas")
        k_hpa = HPA("HPA\n2–5 réplicas al 60 % CPU")
        k_db = STS("StatefulSet db\nPostgreSQL + PostGIS")
        k_pvc = PVC("PVC 2 GiB")
        k_sec = Secret("cells-secrets")
        k_svc >> Edge(label="tráfico", **DATOS) >> k_web
        k_web >> Edge(label="/api", **DATOS) >> k_api
        k_api >> Edge(label="SQL", **DATOS) >> k_db
        k_db >> k_pvc
        k_hpa >> Edge(style="dotted") >> k_api
        k_sec >> Edge(style="dotted") >> k_api

    usuario_k >> Edge(label="HTTP", **DATOS) >> k_svc
    ghcr_k >> Edge(label="imágenes", style="dotted") >> k_web
    ghcr_k >> Edge(style="dotted") >> k_api
