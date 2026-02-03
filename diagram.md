# Simplified Architecture Diagram

This diagram provides a high-level conceptual overview of the federated data architecture, focusing on the primary flow of a request.

```mermaid
graph TD
    User(Client) -- 1. Sends Request --> API[FastAPI Endpoint]
    
    subgraph "Federation Service"
        API -- 2. Calls Orchestrator --> Orchestrator
        Orchestrator -- 3. Scatter Queries --> AdapterLayer[Adapter Layer]
        AdapterLayer -- Fetches From --> DataSources[(Data Sources)]
        DataSources -- Raw Data --> AdapterLayer
        AdapterLayer -- 4. Transform to Unified Schema --> Orchestrator
        Orchestrator -- 5. Gather Results --> API
    end

    API -- 6. Responds with JSON --> User

    style AdapterLayer fill:#D6EAF8,stroke:#333,stroke-width:2px
    style DataSources fill:#D5F5E3,stroke:#333,stroke-width:2px
    style Orchestrator fill:#FDEDEC,stroke:#333,stroke-width:2px
```

### Explanation of the Flow

1.  **Request**: A client sends a request for company data to the public-facing FastAPI Endpoint.
2.  **Orchestration**: The endpoint delegates the work to the Orchestrator.
3.  **Scatter**: The Orchestrator sends out concurrent requests to all registered adapters in the Adapter Layer. Each adapter knows how to communicate with its specific Data Source.
4.  **Transform**: As each adapter receives raw data from its source, it transforms that data into a common, unified Pydantic model.
5.  **Gather**: The Orchestrator waits for all adapters to return their transformed, unified data and gathers the results into a single collection.
6.  **Respond**: The Orchestrator passes the collected data back to the API Endpoint, which formats the final JSON response and sends it to the client.