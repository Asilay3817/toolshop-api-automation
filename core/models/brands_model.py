from pydantic import BaseModel, field_validator

class BrandsModel(BaseModel):
    id: str
    name: str
    slug: str

