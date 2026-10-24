from fastapi import APIRouter

from api.endpoints import health_check

main_router = APIRouter(prefix="/api")

# Define routers
routers = [
    # Health
    (health_check.router, "/health-check", "Health"),
]

for router, prefix, tag in routers:
    main_router.include_router(router, prefix=prefix, tags=[tag])
