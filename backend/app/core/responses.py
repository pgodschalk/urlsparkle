from fastapi.responses import JSONResponse


class HealthJSONResponse(JSONResponse):
    media_type = "application/health+json"
