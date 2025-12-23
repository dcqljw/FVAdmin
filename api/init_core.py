import random
import string

from core.security import get_password_hash
from models.menu_model import Menu
from models.user_model import User

from tortoise import Tortoise


async def create_superuser():
    user = await User.get_or_none(username="admin")
    if not user:
        print("创建超级管理员")
        random_str = string.ascii_lowercase + string.ascii_uppercase + string.digits
        password = "".join(random.choices(random_str, k=8))
        print(f"密码：{password}")
        new_password = get_password_hash(password)
        await User.create(username="admin", password=new_password, nickname="管理员", phone="12345678901",
                          email="admin@admin.com", avatar='')


async def create_menu():
    sql = '''
          INSERT INTO `menu`
          VALUES (5, 0, 'Dashboard', '/dashboard',
                  '{\"icon\": \"ri:pie-chart-line\", \"title\": \"menus.dashboard.title\"}', '/index/index',
                  '2025-12-10 20:28:03.525303', '2025-12-10 22:44:05.402170', 0, 1, '', 1);
          INSERT INTO `menu`
          VALUES (6, 5, 'Console', 'console',
                  '{\"icon\": \"ri:home-smile-2-line\", \"title\": \"menus.dashboard.console\", \"fixedTab\": true, \"keepAlive\": false}',
                  '/dashboard/console', '2025-12-10 20:29:03.932307', '2025-12-10 20:29:03.932307', 0, 1, '', 1);
          INSERT INTO `menu`
          VALUES (7, 0, 'System', '/system', '{\"icon\": \"ri:user-3-line\", \"title\": \"menus.system.title\"}',
                  '/index/index', '2025-12-10 20:30:13.631064', '2025-12-10 20:30:22.414226', 0, 1, '', 1);
          INSERT INTO `menu`
          VALUES (8, 7, 'User', 'user',
                  '{\"icon\": \"ri:user-line\", \"title\": \"menus.system.user\", \"keepAlive\": true}', '/system/user',
                  '2025-12-10 20:31:58.314086', '2025-12-10 20:31:58.314086', 0, 1, '', 1);
          INSERT INTO `menu`
          VALUES (9, 7, 'Role', 'role',
                  '{\"icon\": \"ri:user-line\", \"title\": \"menus.system.role\", \"keepAlive\": true}', '/system/role',
                  '2025-12-10 22:04:36.933778', '2025-12-10 22:04:36.933778', 0, 1, '', 1);
          INSERT INTO `menu`
          VALUES (10, 7, 'UserCenter', 'user-center',
                  '{\"icon\": \"ri:user-line\", \"title\": \"menus.system.userCenter\", \"isHide\": true, \"isHideTab\": true, \"keepAlive\": true}',
                  '/system/user-center', '2025-12-10 22:11:16.721579', '2025-12-10 22:11:16.721579', 0, 1, '', 1);
          INSERT INTO `menu`
          VALUES (11, 7, 'Menus', 'menu', '{\"title\": \"menus.system.menu\", \"keepAlive\": true}', '/system/menu',
                  '2025-12-10 22:12:41.342214', '2025-12-13 19:00:02.988227', 0, 1, 'menu:list', 1);
          INSERT INTO `menu`
          VALUES (12, 8, '', '', '{\"title\": \"新增\"}', '', '2025-12-11 23:32:10.405072',
                  '2025-12-13 21:58:47.498341', 0, 1, 'user:add', 2);
          INSERT INTO `menu`
          VALUES (13, 8, ' ', ' ', '{\"title\": \"删除\"}', ' ', '2025-12-11 23:34:14.344441',
                  '2025-12-13 21:58:58.983669', 0, 1, 'user:delete', 2);
          INSERT INTO `menu`
          VALUES (20, 8, ' ', ' ', '{\"title\": \"修改\"}', ' ', '2025-12-13 21:59:56.264383',
                  '2025-12-13 21:59:56.264383', 0, 1, 'user:edit', 2);
          INSERT INTO `menu`
          VALUES (22, 11, '菜单删除', ' ', '{\"title\": \"删除\"}', ' ', '2025-12-17 13:58:06.010042',
                  '2025-12-17 13:58:06.010042', 0, 1, 'menu:delete', 2);
          INSERT INTO `menu`
          VALUES (23, 0, 'Result', '/result', '{\"icon\": \"\", \"title\": \"result\"}', '/index/index',
                  '2025-12-17 16:52:23.828918', '2025-12-17 16:52:23.828943', 1, 1, '', 1);

          SET
          FOREIGN_KEY_CHECKS = 1;
          '''
    await Tortoise.get_connection('default').execute_script(sql)


async def init_data():
    await create_superuser()
    await create_menu()
