from tortoise.contrib.pydantic import pydantic_model_creator

from models import Tweets, Words


TweetsOutSchema = pydantic_model_creator(
    Tweets, name="TweetsOut", exclude=['id']
)

WordsOutSchema = pydantic_model_creator(
    Words, name="TweetsOut", exclude='id'
)