from fastapi import APIRouter

from app.health.router import router as health_router
from app.todos.router import router as todos_router

router = APIRouter()

# /health
router.include_router(health_router)
# /todos
router.include_router(todos_router)
