from app.errors.api_error import ApiError


class MissingShapefilePartsError(ApiError):
    status_code = 400
    code = "missing_shapefile_parts"
