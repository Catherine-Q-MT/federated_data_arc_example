from pydantic import BaseModel, Field
from typing import Optional

# This file contains the Pydantic models that represent the "raw" data
# structure as it comes from each individual data source.

class SourceACompany(BaseModel):
    company_name: str = Field(alias='company_name')
    company_id: str = Field(alias='company_id')
    location: str = Field(alias='location')
    industry: Optional[str] = Field(default=None)
    employees: Optional[int] = Field(default=None)
    revenue: Optional[str] = Field(default=None)
    founded_year: Optional[int] = Field(default=None)

    class Config:
        populate_by_name = True


class SourceBCompany(BaseModel):
    name: str = Field(alias='name')
    id: int = Field(alias='id')
    street_address: str = Field(alias='street_address')
    city: str = Field(alias='city')
    zip_code: str = Field(alias='zip')
    phone: Optional[str] = Field(default=None)
    website: Optional[str] = Field(default=None)
    region: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    ceo: Optional[str] = Field(default=None)

    class Config:
        populate_by_name = True


class SourceCCompany(BaseModel):
    org_name: str = Field(alias='org_name')
    identifier: str = Field(alias='identifier')
    full_address: str = Field(alias='full_address')
    contact_email: Optional[str] = Field(default=None)
    market_cap: Optional[str] = Field(default=None)
    size: Optional[str] = Field(default=None)
    established: Optional[int] = Field(default=None)
    valuation: Optional[str] = Field(default=None)

    class Config:
        populate_by_name = True
