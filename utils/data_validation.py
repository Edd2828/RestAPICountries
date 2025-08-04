from pydantic import BaseModel, RootModel, field_validator
from typing import List


class CountryDataValidationItemName(BaseModel):
    common: str | None
    official: str | None

    class Config:
        extra = 'ignore'

class CountryDataValidationItem(BaseModel):
    name: CountryDataValidationItemName
    population: int | None

class CountryDataValidation(RootModel):
    root: List[CountryDataValidationItem] | None

    @field_validator('root')
    def check_empty_list(cls, v):
        if not v:
            return [CountryDataValidationItem(name=CountryDataValidationItemName(common=None, official=None), population=None)]
        return v

if __name__ == '__main__':
    pass
    # sample country detail
    # {'name': {'common': 'Azerbaijan', 'official': 'Republic of Azerbaijan'}, 'population': 10000000}