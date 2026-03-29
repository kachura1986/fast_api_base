from fastapi import APIRouter

from .endpoints import health_check
main_router = APIRouter(prefix="/api")

# Define routers
routers = [
    (health_check.router, "/health_check", "API health check"),
]

# Define main router
for router, prefix, tag in routers:
    main_router.include_router(router, prefix=prefix, tags=[tag])
