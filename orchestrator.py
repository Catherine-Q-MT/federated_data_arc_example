import asyncio
from typing import Dict, Optional

from wrappers.base import DataSourceWrapper
from models.models import UnifiedSourceData

class Orchestrator:
    """
    Manages the concurrent execution of data source queries.
    """
    def __init__(self, registry: Dict[str, DataSourceWrapper]):
        self.registry = registry

    async def run(self, company_name_query: str) -> Dict[str, Optional[UnifiedSourceData]]:
        """
        1. Triggers all registered data sources simultaneously.
        2. Gathers the results.
        3. Maps results back to their source names.
        4. Returns the mapped data.
        """
        # 1. Create a list of concurrent tasks
        tasks = [
            adapter.query_by_name(company_name_query)
            for adapter in self.registry.values()
        ]

        # 2. Gather results from all tasks running in parallel
        results = await asyncio.gather(*tasks)

        # 3. Map results back to their source names (e.g., "source_a")
        federated_data = dict(zip(self.registry.keys(), results))
        
        # 4. Return the federated data dictionary
        return federated_data
