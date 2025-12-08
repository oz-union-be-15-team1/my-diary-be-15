from tortoise import Tortoise

async def init_db():
    await Tortoise.init(
        db_url="postgres://user:pass@localhost:5432/app",
        modules={"models": ["app.models"]},
    )
    await Tortoise.generate_schemas()
