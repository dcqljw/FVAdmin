from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ADD INDEX `idx_user_usernam_9987ab` (`username`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` DROP INDEX `idx_user_usernam_9987ab`;"""


MODELS_STATE = (
    "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"
)
