from typing import List, Dict, Any, Optional
from wrappers.base import DataSourceWrapper, extract_country
from models.models import UnifiedSourceData
from models.source_models import SourceCCompany
from data_sources.data_source_c import get_companies_c

class SourceCWrapper(DataSourceWrapper):
    def __init__(self):
        self.data: List[Dict[str, Any]] = get_companies_c()

    async def query_by_name(self, name: str) -> Optional[UnifiedSourceData]:
        for company_data in self.data:
            if name.lower() in company_data.get("org_name", "").lower():
                # 1. Parse
                source_c_parsed = SourceCCompany.model_validate(company_data)

                address_parts = source_c_parsed.full_address.split(',')
                address_line_1 = address_parts[0].strip() if address_parts else ""

                # 2. Transform
                return UnifiedSourceData(
                    name=source_c_parsed.org_name,
                    id=source_c_parsed.identifier,
                    address_line_1=address_line_1,
                    country=extract_country(source_c_parsed.full_address) if source_c_parsed.full_address else None,
                    industry=None # Not available from this source
                )
        return None
