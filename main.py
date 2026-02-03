from fastapi import FastAPI, HTTPException

# Import the Pydantic model for the final response
from models.models import FederatedCompanyView
# Import the wrapper classes
from wrappers import SourceAWrapper, SourceBWrapper, SourceCWrapper
# Import the new Orchestrator
from orchestrator import Orchestrator

app = FastAPI(
    title="Federated Data Service",
    description="An API using an async orchestrator to query multiple data sources concurrently."
)

# --- Adapter Instantiation and Registry ---
ADAPTER_REGISTRY = {
    "source_a": SourceAWrapper(),
    "source_b": SourceBWrapper(),
    "source_c": SourceCWrapper(),
}

# --- Orchestrator Instantiation ---
# The orchestrator is initialized with the registry of all available adapters.
data_orchestrator = Orchestrator(registry=ADAPTER_REGISTRY)


@app.get("/companies/{company_name_query}", response_model=FederatedCompanyView, tags=["Companies"])
async def get_federated_company_data(company_name_query: str):
    """
    Retrieves and federates company data by calling an orchestrator
    that queries data sources concurrently.
    """
    # 1. & 2. & 3. Trigger all sources, gather, and map results
    federated_data = await data_orchestrator.run(company_name_query)

    # Check if any data was found
    if not any(federated_data.values()):
        raise HTTPException(status_code=404, detail=f"No data found for company: {company_name_query}")

    # 4. Format and Return the final response
    response = FederatedCompanyView(
        company=company_name_query,
        **federated_data
    )

    return response


@app.get("/companies", tags=["Companies"])
async def list_companies():
    """
    Lists company names available from Source A to use in queries.
    """
    from data_sources.data_source_a import get_companies_a
    return {"available_companies": [c.get("company_name") for c in get_companies_a()]}
