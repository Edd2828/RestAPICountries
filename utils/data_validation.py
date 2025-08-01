from pydantic import BaseModel, RootModel
from typing import List


class CountryDataValidationItemName(BaseModel):
    common: str
    official: str

    class Config:
        extra = 'ignore'

class CountryDataValidationItem(BaseModel):
    name: CountryDataValidationItemName
    population: int

class CountryDataValidation(RootModel):
    root: List[CountryDataValidationItem]