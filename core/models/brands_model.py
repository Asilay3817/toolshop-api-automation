from pydantic import BaseModel, TypeAdapter

class BrandsModel(BaseModel):
    id: str
    name: str
    slug: str

    @classmethod
    def parse_list(cls, response) -> list["BrandsModel"]:
        """
        Parse the API response into a list of BrandsModel objects
        """
        return TypeAdapter(list[cls]).validate_python(response.json())