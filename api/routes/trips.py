from fastapi import APIRouter, HTTPException

from api.schemas import TripRequest
from agents.planner import PlannerAgent
from api.schemas import TripRequest, TripResponse


router = APIRouter(
    prefix="/api/trips",
    tags=["Trips"]
)


@router.post("/", response_model=TripResponse)
def create_trip(request: TripRequest):

    planner = PlannerAgent()

    try:

        result = planner.run(
            request.user_request
        )

        if not result:

            raise HTTPException(
                status_code=404,
                detail="No trip result generated"
            )

        return {
            "success": True,
            "data": result
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )