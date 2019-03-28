class BadRequest(Exception):
    """Ошибка, при неправильном запросе (соответствует HTTP 400)"""
    http_code = 400


class PermissionDenied(Exception):
    """
    Ошибка гененрирутся, когда пользователь не имеет
    права на выполнениедействия (соответствует HTTP 403)
    """
    http_code = 403
