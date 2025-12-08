from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "password_hash" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "tokenblacklist" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token" TEXT NOT NULL,
    "expired_at" TIMESTAMPTZ NOT NULL,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "diary" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(100) NOT NULL,
    "content" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "owner_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "quote" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "content" TEXT NOT NULL,
    "author" VARCHAR(100)
);
CREATE TABLE IF NOT EXISTS "question" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "question_text" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "userquestion" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "answer_content" TEXT,
    "answered_at" TIMESTAMPTZ,
    "question_id" INT NOT NULL REFERENCES "question" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_userquestio_user_id_e2c439" UNIQUE ("user_id", "question_id")
);
CREATE TABLE IF NOT EXISTS "bookmark" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "quote_id" INT NOT NULL REFERENCES "quote" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_bookmark_user_id_46416a" UNIQUE ("user_id", "quote_id")
);
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
    "eJztWttu2zgU/BVBTy2QDRI3bgujWMBxnDbbxtkm2t2iRSHQ0rFNWCYVkqptZPPvBan7zY"
    "0cK7UQvdnkORQ5lM6MhrrTF9QGhx8adA7k1EHW3MFc6D3tTidoAXpPK4k40HTkunG/bBBo"
    "7KgUIWPHqdgxFwxZcuQJcjgcaLoN3GLYFZgSvacRz3FkI7W4YJhM4yaP4FsPTEGnIGbA9J"
    "727fuBpmNiwwp4+NedmxMMjp2aOrbltVW7Kdauarsg4lwFyquNTYs63oLEwe5azCiJojFR"
    "058CAYYEyOEF8+T05eyC9YYr8mcah/hTTOTYMEGeIxLLfSAGFiUSP0yEXPCdPpVX+aNzfP"
    "Lm5O2r1ydvDzRdzSRqeXPvLy9eu5+oEBgZ+r3qRwL5EQrGGDe1f3noDFiVYBclZODjgmXh"
    "C8HahF/YEAMY3zS7QXADPMbwiyEnveD81pENo3/714MP/esXl/0vL1XPOuj5dDV6H4ZThi"
    "z/7h8NPl2dKoRjRGHlYga2iUQe1jMkQOAFFEObzszgaweph+GPutDW3008YkmUtRElcOgJ"
    "i9Dln3o9O3BxObwx+pd/p7bhrG8MZU8ntQVh64vXL9O7EA2i/XdhfNDkX+3r1WioUKRcTJ"
    "m6YhxnfNXlnJAnqEno0kR2EoqwOWxK7a7HgZmVik0i49cVZz8emV0UHVmpJ/PCmiMRyQN4"
    "ThngKfkIa4XjBeECEQsKcAto6p9gmP3DLwAnbo15gaFlxF7JW4MS0wYHhFrgoH8z6J8NdQ"
    "XiGFnzJWK2mUJT9tAOzbREsfmuRWeRbUEETdX65SrknJPAFuiCEPByNRDubKsBmqQB5K6p"
    "3zn0BjPEyqtamLMbJVA7igu0Mh0gUzHTe1r3aANkoQroHmWYJtQHHdWV5n0Xcb6kzDZniM"
    "+qQJlLbIqySiPa6XYfAGmn2y3FVPUVMEd5FczoWBOIYBh4Hv3TIP384zU4SC20lFfyrz/N"
    "YZjUHWlj9Hg0zjBi6waDgDjHUwK2eesBl1d4JB6SBD8HQzUYljGl8wVi80eicRoM0zAk6l"
    "RP/gNTIJ+iJ6lcP9lRSCugGiSgBBZOJfUUJTST6o+PHqKejo/K5ZPqS+snixIB/u3zUC8q"
    "kdIUIJ/ajbIYyPVv4UalM1s3ah/dKLokVe2oZErrR8UotoZU5ubYJ0fqs0fVPHKayu/YqK"
    "luo5BWUzVIU7VyoA45gDwxo6yKVI0ztsI0uOuaL1W3cqXat+z6GCGwYApJIbZnNvFCIqql"
    "hgZRQ7hzpoBVJYLIJbY0EdPEVgUuclfledDzdVbrPo3dVO2ysG0+na2v6n2LTn+ja3xvK2"
    "G9lRARvgRmbqGV85kNkXdPrpgVUFs5aJnUHVho+wV309yyiP4rlZtM1nPyzNoP39oP337P"
    "h29Fj+0OkGumvMyil6lI+2TURk5FgVBNuhjlIjW0TOoVqNISbtVp7e/pVEBVso1TnhNptE"
    "zbMu0+MG1wVPZomg3GaS5uyUK0TwTbB4atWRG9Bj0byRXFMa3j3SAm/QGMFyrg8nO7RMoz"
    "/5485ea4bqXDTz+8mQA+7Vd6f91cjaoey9vYEtr/2t5/Zj8pwE+ud7PZmPUVM46WHKDiuc"
    "vuieX+J8IqCZM="
)
