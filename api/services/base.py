from custom_exception import CustomException


class BaseService:
    """基础 Service，提供通用异常抛出方法"""

    @staticmethod
    def _not_found(entity_name: str, identifier: str):
        raise CustomException(code=400, msg=f"{entity_name}不存在: {identifier}")

    @staticmethod
    def _already_exists(entity_name: str, identifier: str):
        raise CustomException(code=400, msg=f"{entity_name}已存在: {identifier}")

    @staticmethod
    def _forbidden(msg: str):
        raise CustomException(code=403, msg=msg)
