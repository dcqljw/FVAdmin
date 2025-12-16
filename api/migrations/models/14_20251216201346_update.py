from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `role` MODIFY COLUMN `enabled` BOOL NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `role` MODIFY COLUMN `enabled` INT NOT NULL;"""


MODELS_STATE = (
    "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"
    "JLhUOr8zFU/5paBJvBQURE1e/gN+D751"
)
