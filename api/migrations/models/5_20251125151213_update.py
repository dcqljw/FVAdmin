from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ADD UNIQUE INDEX `username` (`username`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` DROP INDEX `username`;"""


MODELS_STATE = (
    "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"
)
