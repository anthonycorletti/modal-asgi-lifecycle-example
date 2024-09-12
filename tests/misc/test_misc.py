from app.settings import settings


async def test_settings_env_check() -> None:
    assert settings.is_test()
    assert not settings.is_local()
    assert not settings.is_preview()
