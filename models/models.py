from pydantic import BaseModel
from typing import Optional

# This file contains the Pydantic models that define the "public" or
# "unified" data structure that the API exposes to consumers.

# --- Unified Source Data Model ---
# This model defines the consistent shape for each source's data within the federated output.
class UnifiedSourceData(BaseModel):
    name: str
    id: str
    address_line_1: str
    country: Optional[str] = None
    industry: Optional[str] = None


# --- Federated Output Model ---
# This is the final structure that will be returned to the user.
class FederatedCompanyView(BaseModel):
    company: str
    source_a: Optional[UnifiedSourceData] = None
    source_b: Optional[UnifiedSourceData] = None
    source_c: Optional[UnifiedSourceData] = None
