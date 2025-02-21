from fastapi import APIRouter

from app.api.routes import healthz, readyz, shorten, update
from app.api.routes.shortcode import _, stats

api_router = APIRouter()
api_router.include_router(healthz.router)
api_router.include_router(readyz.router)
api_router.include_router(_.router)
api_router.include_router(shorten.router)
api_router.include_router(stats.router)
api_router.include_router(update.router)
