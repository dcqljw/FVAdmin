from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `menu` ADD `auth_mark` VARCHAR(255) NOT NULL COMMENT '按钮权限标识';
        ALTER TABLE `menu` ADD `type` INT NOT NULL COMMENT '类型 1菜单2按钮' DEFAULT 1;
        ALTER TABLE `menu` MODIFY COLUMN `name` VARCHAR(255) NOT NULL COMMENT '菜单名称|按钮名称';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `menu` DROP COLUMN `auth_mark`;
        ALTER TABLE `menu` DROP COLUMN `type`;
        ALTER TABLE `menu` MODIFY COLUMN `name` VARCHAR(255) NOT NULL COMMENT '菜单名称';"""


MODELS_STATE = (
    "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"
    "00oFQ5cTMTQ/mlQEm8FJRESp7+BzMXsHo="
)
