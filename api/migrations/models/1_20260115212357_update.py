from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ALTER COLUMN `avatar` SET DEFAULT '';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ALTER COLUMN `avatar` DROP DEFAULT;"""


MODELS_STATE = (
    "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"
    "w="
)
