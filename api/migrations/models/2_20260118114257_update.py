from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `apikey` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `key` VARCHAR(100) NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `apikey`;"""


MODELS_STATE = (
    "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"
)
