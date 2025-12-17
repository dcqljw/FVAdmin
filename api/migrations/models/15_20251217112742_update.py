from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `menu` MODIFY COLUMN `status` BOOL NOT NULL COMMENT '状态' DEFAULT 1;
        ALTER TABLE `user` MODIFY COLUMN `status` BOOL NOT NULL COMMENT '状态' DEFAULT 1;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `menu` MODIFY COLUMN `status` INT NOT NULL COMMENT '状态' DEFAULT 1;
        ALTER TABLE `user` MODIFY COLUMN `status` INT NOT NULL COMMENT '状态' DEFAULT 1;"""


MODELS_STATE = (
    "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"
)
