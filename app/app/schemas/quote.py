from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.quote import Quote

Quote_Pydantic = pydantic_model_creator(
    Quote,
    name="Quote"
)
