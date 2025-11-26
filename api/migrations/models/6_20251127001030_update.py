from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `role` ADD UNIQUE INDEX `name` (`name`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `role` DROP INDEX `name`;"""


MODELS_STATE = (
    "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"
)
