from core.exceptions import CustomException

# 超级管理员标识（全系统唯一引用，禁止散落魔法字符串）
SUPERADMIN_USERNAME = "superadmin"
SUPERADMIN_ROLE_CODE = "R_ADMIN"


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

    def _ensure_not_superadmin(self, username: str):
        """用户名是超级管理员时抛出 403"""
        if username == SUPERADMIN_USERNAME:
            self._forbidden("超级管理员不允许操作")

    def _ensure_not_admin_role(self, role_code: str):
        """角色 code 是超级管理员时抛出 403"""
        if role_code == SUPERADMIN_ROLE_CODE:
            self._forbidden("超级管理员角色不允许操作")

    def _ensure_no_admin_role_assign(self, role_codes: list):
        """角色列表中含有超级管理员角色时抛出 403"""
        if SUPERADMIN_ROLE_CODE in role_codes:
            self._forbidden("不允许分配超级管理员角色")
