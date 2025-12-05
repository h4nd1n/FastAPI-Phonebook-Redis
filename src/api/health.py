from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get(
    "",
    status_code=200,
    summary="Проверка здоровья",
    responses={200: {"description": "Сервис работает"}},
)
async def health():
    return {"status": "ok"}
