class ApiError(Exception):
    status_code = 400
    code = "bad_request"

    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail
