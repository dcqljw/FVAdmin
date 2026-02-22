from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "llmmodel" RENAME COLUMN "baseUrl" TO "base_url";
        ALTER TABLE "llmmodel" RENAME COLUMN "apiKey" TO "api_key";
        ALTER TABLE "llmmodel" ADD "model" VARCHAR(100) NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "llmmodel" RENAME COLUMN "base_url" TO "baseUrl";
        ALTER TABLE "llmmodel" RENAME COLUMN "api_key" TO "apiKey";
        ALTER TABLE "llmmodel" DROP COLUMN "model";"""


MODELS_STATE = (
    "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"
)
