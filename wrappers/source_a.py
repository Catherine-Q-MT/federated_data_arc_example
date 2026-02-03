from typing import List, Dict, Any, Optional
from wrappers.base import DataSourceWrapper, extract_country
from models.models import UnifiedSourceData
from models.source_models import SourceACompany
from data_sources.data_source_a import get_companies_a

class SourceAWrapper(DataSourceWrapper):
    def __init__(self):
        self.data: List[Dict[str, Any]] = get_companies_a()

    async def query_by_name(self, name: str) -> Optional[UnifiedSourceData]:
        for company_data in self.data:
            if name.lower() in company_data.get("company_name", "").lower():
                # 1. Parse raw data into its specific Pydantic model
                source_a_parsed = SourceACompany.model_validate(company_data)
                
                # 2. Transform into the UnifiedSourceData model
                return UnifiedSourceData(
                    name=source_a_parsed.company_name,
                    id=source_a_parsed.company_id,
                    address_line_1=source_a_parsed.location.split(',')[0].strip() if source_a_parsed.location else "",
                    country=extract_country(source_a_parsed.location) if source_a_parsed.location else None,
                    industry=source_a_parsed.industry
                )
        return None
