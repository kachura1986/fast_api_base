from fastapi import APIRouter

from api.endpoints import health_check

main_router = APIRouter(prefix="/api")

# Define routers
routers = [
    (health_check.router, "/health_check", ["Health"]),
]

for router, prefix, tags in routers:
    main_router.include_router(router, prefix=prefix, tags=tags)
