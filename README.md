# 🤖 Agentic RAG Architecture: Dockerized & Cloud-Agnostic

> **Sistema de Inteligencia Artificial Agéntica (RAG) desplegado en microservicios contenerizados. Diseño resiliente, escalable y agnóstico a la nube.**

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![AI](https://img.shields.io/badge/AI-Llama%203.3-orange?logo=meta&logoColor=white)
![DB](https://img.shields.io/badge/Vector%20DB-Qdrant-red)

## 🏗️ Arquitectura del Sistema

Este proyecto implementa una arquitectura **Cloud-Native** desacoplada. Utiliza **Docker Compose** para la orquestación de servicios y **Docker Volumes** para garantizar la persistencia de datos vectoriales.

```mermaid
graph TD
    User((👤 Usuario))

    subgraph Docker_Host ["Docker Host (Tu Servidor)"]
        style Docker_Host fill:#f9f9f9,stroke:#333,stroke-width:2px

        subgraph Docker_Network ["Docker Network: ai-network (Bridge)"]
            style Docker_Network fill:#e1f5fe,stroke:#0277bd,stroke-dasharray: 5 5

            Frontend["🖥️ Container: ai-frontend<br/>(Streamlit)"]
            API["⚙️ Container: ai-api<br/>(FastAPI)"]
            DB["🗄️ Container: qdrant-db<br/>(Vector DB)"]
        end

        Volume["💾 Host Volume:<br/>./qdrant_data"]
    end

    %% Flujos de Comunicación
    User -- "Browser HTTP: 8501" --> Frontend
    Frontend -- "Internal DNS:<br/>http://ai-api:8000" --> API
    API -- "Internal DNS:<br/>http://qdrant:6333" --> DB

    %% Persistencia
    DB -.-> Volume
```

## 🛠️ Tech Stack

*   **Frontend:** Streamlit (Interfaz de Chat Reactiva).
*   **Backend API:** FastAPI (Microservicio REST).
*   **Vector Database:** Qdrant (Almacenamiento Semántico Persistente).
*   **GenAI Engine:** Groq API (Inferencia Llama 3.3-70b).
*   **Infraestructura:** Docker Compose, Docker Networks, Volumes.

## 🚀 Guía de Despliegue (Quickstart)

### Requisitos
*   Docker & Docker Compose instalados.
*   API Key de Groq (Gratuita).

### 1. Clonar el repositorio
```bash
git clone https://github.com/KorbenDallas007/agente-rag-docker.git
cd agente-rag-docker
```

### 2. Despliegue de Infraestructura
Levanta todo el stack con un solo comando. El sistema construirá las imágenes y conectará la red automáticamente.

```bash
docker compose up --build -d
```

Verifica que los 3 servicios estén corriendo:
```bash
docker compose ps
```

### 3. Ingesta de Conocimiento (ETL)
Carga los documentos base en la memoria vectorial (Qdrant).
*Nota: Este script se ejecuta localmente y se conecta a la infraestructura vía puertos expuestos.*

```bash
# (Opcional) Crea un entorno virtual
pip install -r requirements.txt

# Ejecutar ETL
python3 etl_pipeline.py
```

### 4. Acceder al Sistema
*   **Frontend Web:** Abre tu navegador en `http://localhost:8501`
*   **API Docs:** `http://localhost:8080/docs`
*   **Qdrant Dashboard:** `http://localhost:6333/dashboard`

## 📸 Demo

<img width="786" height="833" alt="image" src="https://github.com/user-attachments/assets/ea4fd948-7249-4b99-b88e-f24bd02bd31a" />


## 🧠 Características Avanzadas

*   **Persistencia de Datos:** El sistema utiliza volúmenes de Docker (`./qdrant_data`), lo que permite que la "memoria" de la IA sobreviva a reinicios o caídas de contenedores.
*   **Service Discovery:** Los microservicios se comunican mediante DNS interno de Docker, eliminando la dependencia de IPs fijas.
*   **Configuración Dinámica:** El Frontend lee variables de entorno (`API_URL`, `QDRANT_URL`) para adaptarse a entornos de Desarrollo o Producción.
*   **Deterministic Embedding Simulation:** Implementación de un algoritmo de hashing determinista para simular embeddings sin consumo excesivo de RAM en entornos limitados.

---
*Desarrollado por [KorbenDallas007](https://github.com/KorbenDallas007) - AI Solutions Architect Portfolio.*
```
