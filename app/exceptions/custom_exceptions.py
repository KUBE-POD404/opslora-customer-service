class AppException(Exception):
    def _init_(self, message: str, status_code: int = 400, details: dict | None = None):
        self.message = message
        self.status_code = status_code
        self.details = details


class NotFoundException(AppException):
    def _init_(self, message="Resource not found"):
        super()._init_(message, 404)


class UnauthorizedException(AppException):
    def _init_(self, message="Unauthorized"):
        super()._init_(message, 401)


class ForbiddenException(AppException):
    def _init_(self, message="Forbidden"):
        super()._init_(message, 403)


class ConflictException(AppException):
    def _init_(self, message="Conflict"):
        super()._init_(message, 409)
