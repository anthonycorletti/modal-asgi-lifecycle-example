import json
from typing import Dict

from fastapi import FastAPI
from modal import App, Image, Secret, asgi_app

from app.settings import settings

app = App(name="modal-asgi-lifecycle-example")

_app_env_dict: Dict[str, str | None] = {
    f"APP_{str(k)}": str(v) for k, v in json.loads(settings.model_dump_json()).items()
}
app_env = Secret.from_dict(_app_env_dict)

image = (
    Image.debian_slim()
    .pip_install("uv")
    .workdir("/work")
    .copy_local_file("pyproject.toml", "/work/pyproject.toml")
    .copy_local_file("uv.lock", "/work/uv.lock")
    .env({"UV_PROJECT_ENVIRONMENT": "/usr/local"})
    .run_commands(
        [
            "uv sync --frozen --compile-bytecode",
            "uv build",
        ]
    )
)


@app.function(image=image, secrets=[app_env])
@asgi_app(label="app")
def _app() -> FastAPI:
    from app.main import app

    return app
