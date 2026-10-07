from fastapi import FastAPI

from app.errors.register_error_handlers import register_error_handlers
from app.routes import check_health, get_file_info, get_file_measurements, upload_file


def create_app() -> FastAPI:
    app = FastAPI(title="Geospatial File Measurement API")
    for module in (upload_file, get_file_info, get_file_measurements, check_health):
        app.include_router(module.router)
    register_error_handlers(app)
    return app


app = create_app()
