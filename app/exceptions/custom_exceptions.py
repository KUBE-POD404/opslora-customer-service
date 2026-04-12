class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400, details: dict | None = None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message, status_code, details)


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found", details: dict | None = None):
        super().__init__(message, 404, details)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized", details: dict | None = None):
        super().__init__(message, 401, details)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden", details: dict | None = None):
        super().__init__(message, 403, details)


class ConflictException(AppException):
    def __init__(self, message: str = "Conflict", details: dict | None = None):
        super().__init__(message, 409, details)