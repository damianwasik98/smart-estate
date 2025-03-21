from pydantic import BaseModel, Field


class LLMClientRequirements(BaseModel):
    location: str = Field(
        ...,
        description="Desired location of property",
    )
    note: str | None = Field(
        None,
        description="if there is some additional info, not associated with other schema fields, it should go here",
        examples=[
            "clients needs as meeting schedule, or that he wants to buy this month"
        ],
    )
    area_min: int | None = Field(
        None, description="Desired property minimum area (in m2)"
    )
    area_max: int | None = Field(
        None, description="Desired proparty maximum area (in m2)"
    )
    price_max: int | None = Field(
        None, description="Maximum price that client is willing to pay for property"
    )
    no_of_rooms_min: int | None = Field(
        None, description="Minimal rooms count in property"
    )
    no_of_rooms_max: int | None = Field(
        None, description="Maximum rooms count in property"
    )
    floor_no_min: int | None = Field(None, description="Minimal property floor number")
    floor_no_max: int | None = Field(None, description="Maximum property floor number")
    year_built_min: int | None = Field(
        None, description="Properties that were built later than"
    )
    year_built_max: int | None = Field(
        None, description="Properties that were built sooner than"
    )


class ClientRequirements(BaseModel):
    phone_number: str
    first_name: str
    location: str
    last_name: str | None = None
    note: str | None = None
    area_min: int | None = None
    area_max: int | None = None
    price_max: int | None = None
    no_of_rooms_min: int | None = None
    no_of_rooms_max: int | None = None
    floor_no_min: int | None = None
    floor_no_max: int | None = None
    year_built_min: int | None = None
    year_built_max: int | None = None
