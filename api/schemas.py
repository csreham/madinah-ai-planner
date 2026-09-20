from pydantic import BaseModel, Field


class TripRequest(BaseModel):

    user_request: str = Field(
        ...,
        min_length=3,
        description="User's tourism trip request"
    )


class TripData(BaseModel):

    city: str

    days: int

    weather: dict

    hotels: list

    restaurants: list

    places: list

    schedule: dict

    transportation: dict

    budget: dict


class TripResponse(BaseModel):

    success: bool

    data: TripData