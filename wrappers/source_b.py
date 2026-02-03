from typing import List, Dict, Any, Optional
from wrappers.base import DataSourceWrapper
from models.models import UnifiedSourceData
from models.source_models import SourceBCompany
from data_sources.data_source_b import get_companies_b

class SourceBWrapper(DataSourceWrapper):
    def __init__(self):
        self.data: List[Dict[str, Any]] = get_companies_b()

    async def query_by_name(self, name: str) -> Optional[UnifiedSourceData]:
        for company_data in self.data:
            if name.lower() in company_data.get("name", "").lower():
                # 1. Parse
                source_b_parsed = SourceBCompany.model_validate(company_data)
                
                # 2. Transform
                return UnifiedSourceData(
                    name=source_b_parsed.name,
                    id=str(source_b_parsed.id),
                    address_line_1=source_b_parsed.street_address,
                    country=None, # Not available from this source
                    industry=None # Not available from this source
                )
        return None
