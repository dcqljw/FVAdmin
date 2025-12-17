from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` MODIFY COLUMN `status` INT NOT NULL COMMENT '状态' DEFAULT 1;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` MODIFY COLUMN `status` BOOL NOT NULL COMMENT '状态' DEFAULT 1;"""


MODELS_STATE = (
    "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"
)
