from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `menu` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `parent_id` INT NOT NULL COMMENT '父级id' DEFAULT 0,
    `name` VARCHAR(255) NOT NULL COMMENT '菜单名称|按钮名称',
    `type` INT NOT NULL COMMENT '类型 1菜单2按钮' DEFAULT 1,
    `path` VARCHAR(255) NOT NULL COMMENT '菜单路径',
    `auth_mark` VARCHAR(255) NOT NULL COMMENT '按钮权限标识',
    `meta` JSON COMMENT '菜单元数据',
    `sort` INT NOT NULL COMMENT '排序' DEFAULT 0,
    `status` BOOL NOT NULL COMMENT '状态' DEFAULT 1,
    `component` VARCHAR(255) NOT NULL COMMENT '页面路径',
    `created_at` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `permission` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `code` VARCHAR(255) NOT NULL,
    `description` VARCHAR(255) NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `role` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL UNIQUE,
    `code` VARCHAR(255) NOT NULL UNIQUE,
    `description` VARCHAR(255) NOT NULL,
    `enabled` BOOL NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(255) NOT NULL UNIQUE COMMENT '用户名',
    `nickname` VARCHAR(255) NOT NULL COMMENT '昵称',
    `password` VARCHAR(255) NOT NULL COMMENT '密码',
    `email` VARCHAR(255) NOT NULL COMMENT '邮箱',
    `phone` VARCHAR(11) NOT NULL COMMENT '手机号',
    `avatar` VARCHAR(255) NOT NULL COMMENT '头像',
    `status` INT NOT NULL COMMENT '状态' DEFAULT 1,
    `created_at` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    KEY `idx_user_usernam_9987ab` (`username`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `role_menu` (
    `role_id` INT NOT NULL,
    `menu_id` INT NOT NULL,
    FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uidx_role_menu_role_id_90801c` (`role_id`, `menu_id`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user_role` (
    `user_id` INT NOT NULL,
    `role_id` INT NOT NULL,
    FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uidx_user_role_user_id_d0bad3` (`user_id`, `role_id`)
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
)
