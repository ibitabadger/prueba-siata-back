class NotFoundError(Exception):
    """Recurso no encontrado (mapeable a 404)."""


class DuplicateError(Exception):
    """Recurso duplicado (mapeable a 400)."""


class UnauthorizedError(Exception):
    """No autorizado (mapeable a 401)."""


class ConflictError(Exception):
    """Conflicto de integridad (mapeable a 409)."""
