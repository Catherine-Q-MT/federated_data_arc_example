# Federated Data Service

This project demonstrates a basic federated data architecture pattern using FastAPI, Pydantic, and an asynchronous orchestrator. It allows you to query company data that is distributed across multiple "mock" data sources, presenting it to the user in a single, unified, and consistent format.

## Architecture Overview

The system is designed with modularity and scalability in mind, separating concerns into distinct components:

-   **Data Sources (`data_sources/`)**: These are simple Python files simulating external systems or databases. Each provides raw, heterogeneous company data.
-   **Models (`models/`)**:
    -   `models/source_models.py`: Defines Pydantic models for the raw, source-specific data formats. These models act as internal contracts for each adapter.
    -   `models/models.py`: Defines the `UnifiedSourceData` Pydantic model (the consistent format for data from any single source) and the `FederatedCompanyView` model (the final, combined response structure).
-   **Adapters/Wrappers (`wrappers/`)**:
    -   A `DataSourceWrapper` base class defines a common asynchronous interface.
    -   Concrete adapters (`SourceAWrapper`, `SourceBWrapper`, `SourceCWrapper`) encapsulate the logic for fetching data from their respective raw data sources and transforming it into the `UnifiedSourceData` format.
-   **Orchestrator (`orchestrator.py`)**: This component is responsible for:
    1.  **Concurrent Execution**: Firing off asynchronous calls to all active data source adapters simultaneously.
    2.  **Aggregation**: Waiting for all adapters to return their results (or indicate no data found).
    3.  **Mapping**: Collecting the results and mapping them back to their corresponding source names.
-   **FastAPI Application (`main.py`)**: The main entry point. It hosts the API endpoints, initializes the adapter registry and the orchestrator, and coordinates the request flow by calling the orchestrator and returning the final, federated JSON response.

### Key Benefits of this Architecture

-   **Modularity**: Clear separation of concerns, making components easier to develop, test, and maintain independently.
-   **Scalability**: New data sources can be added by simply creating a new adapter and registering it, without modifying the core API endpoint logic.
-   **Asynchronous Processing**: Queries to multiple data sources are executed concurrently, significantly improving response times compared to sequential execution, especially with network-bound operations.
-   **Data Consistency**: Pydantic models enforce a unified data structure, ensuring consumers always receive data in an expected format regardless of the underlying source's schema.

## Local Setup

To set up the project locally for development, it's recommended to use `uv` for dependency management:

1.  **Ensure Python 3.9+ is installed.**
2.  **Install `uv`**:
    ```bash
    pip install uv
    ```
3.  **Install dependencies**:
    ```bash
    uv pip install -r requirements.txt
    ```

## How to Run with Docker

The application is containerized for easy deployment and execution.

1.  **Build the Docker image:**
    Navigate to the project's root directory in your terminal and run:
    ```bash
    docker build -t federated-api .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -d -p 8000:8000 --name my-federated-app federated-api
    ```
    This command runs the container in detached mode (`-d`), maps port 8000 of your host to port 8000 in the container (`-p 8000:8000`), and names the container `my-federated-app`.

3.  **Access the API documentation:**
    Once the container is running, open your web browser and navigate to the interactive API documentation at:
    [http://localhost:8000/docs](http://localhost:8000/docs)

    You can use the `/companies` endpoint to see available company names for querying.

4.  **Example Query:**
    To get federated data for a company, e.g., "Alpha Corp", visit:
    [http://localhost:8000/companies/Alpha%20Corp](http://localhost:8000/companies/Alpha%20Corp)

## Stopping and Cleaning Up

To manage the Docker container and image:

-   **Stop the running container:**
    ```bash
    docker stop my-federated-app
    ```
-   **Remove the container (after stopping):**
    ```bash
    docker rm my-federated-app
    ```
-   **Remove the Docker image:**
    ```bash
    docker rmi federated-api
    ```