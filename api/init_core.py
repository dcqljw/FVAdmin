from tortoise.exceptions import IntegrityError

from core.security import get_password_hash
from shared.base_service import SUPERADMIN_USERNAME, SUPERADMIN_ROLE_CODE
from shared.log_config import app_logger
from shared.utils import generate_random_password
from modules.system.models import Role, User


async def create_superuser():
    """
    初始化超级管理员账号（随机密码，输出到控制台）。
    菜单和角色由 seed.py 负责创建，此处仅负责创建用户并关联超级管理员角色。
    """
    user = await User.get_or_none(username=SUPERADMIN_USERNAME)
    if not user:
        app_logger.info("创建超级管理员")
        password = generate_random_password()
        app_logger.info(f"超级管理员初始密码：{password}")
        new_password = get_password_hash(password)
        user = await User.create(
            username=SUPERADMIN_USERNAME,
            password=new_password,
            nickname="管理员",
            phone="12345678901",
            email="admin@admin.com",
            avatar="",
        )
        app_logger.info("超级管理员创建成功")
    else:
        app_logger.info("超级管理员已存在，跳过创建")

    # 确保超级管理员始终关联 R_ADMIN 角色（幂等）
    admin_role = await Role.get_or_none(code=SUPERADMIN_ROLE_CODE)
    if not admin_role:
        app_logger.warning(f"角色 {SUPERADMIN_ROLE_CODE} 不存在，请先执行 seed.py 初始化数据")
        return
    try:
        await user.roles.add(admin_role)
    except IntegrityError:
        pass  # 已关联，跳过


async def init_data():
    app_logger.info("开始初始化系统数据")
    await create_superuser()
    app_logger.info("系统数据初始化完成")