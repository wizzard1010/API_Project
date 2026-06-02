from litestar import get,Router


@get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
