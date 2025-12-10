from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "password_hash" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255)
);
COMMENT ON TABLE "user" IS 'USERS 테이블';
CREATE TABLE IF NOT EXISTS "diary" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(100) NOT NULL,
    "content" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "owner_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "diary" IS 'DIARIES 테이블 (User → Diary: 1:N 관계)';
CREATE TABLE IF NOT EXISTS "tokenblacklist" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token" TEXT NOT NULL,
    "expired_at" TIMESTAMPTZ,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "tokenblacklist" IS 'TokenBlacklist 테이블의 역할:';
CREATE TABLE IF NOT EXISTS "quote" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "content" TEXT NOT NULL,
    "author" VARCHAR(100)
);
COMMENT ON TABLE "quote" IS 'QUOTES 테이블';
CREATE TABLE IF NOT EXISTS "bookmark" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "quote_id" INT NOT NULL REFERENCES "quote" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_bookmark_user_id_46416a" UNIQUE ("user_id", "quote_id")
);
COMMENT ON TABLE "bookmark" IS 'BOOKMARKS 테이블 (N:M 관계를 위한 중간 테이블)';
CREATE TABLE IF NOT EXISTS "question" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "question_text" TEXT NOT NULL
);
COMMENT ON TABLE "question" IS 'QUESTIONS 테이블';
CREATE TABLE IF NOT EXISTS "userquestion" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "answer_content" TEXT,
    "answered_at" TIMESTAMPTZ,
    "question_id" INT NOT NULL REFERENCES "question" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_userquestio_user_id_e2c439" UNIQUE ("user_id", "question_id")
);
COMMENT ON TABLE "userquestion" IS 'USER_QUESTIONS 테이블';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
)
