from abc import ABC, abstractmethod
from typing import Optional
from models.models import UnifiedSourceData

class DataSourceWrapper(ABC):
    """Abstract base class for a data source wrapper."""
    @abstractmethod
    async def query_by_name(self, name: str) -> Optional[UnifiedSourceData]:
        """
        Asynchronously queries the data source for a company by name and returns
        the data transformed into the UnifiedSourceData model.
        """
        pass

def extract_country(address: str) -> Optional[str]:
    """A simple helper to extract a country from an address string."""
    if "USA" in address.upper():
        return "USA"
    return None
