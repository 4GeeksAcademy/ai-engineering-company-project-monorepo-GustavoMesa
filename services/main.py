from fastapi import FastAPI

from src.inventory.router import router as inventory_router

app = FastAPI(
    title="Brasaland Services",
    description="API interna para las operaciones de Brasaland.",
    version="1.0.0",
)

app.include_router(inventory_router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
