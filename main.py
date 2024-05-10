from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, Depends, HTTPException, status
from tweets import get_tweets as get_tweets_func
from words import get_word_frequency
from schemes import TweetsOutSchema
from datetime import date as date_type
router = APIRouter()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.get('/get_tweets', response_model=TweetsOutSchema)
async def get_tweets(lang: str = '', type: str = '', group: str='week', from_: date_type='2024-01-01', to_: date_type=date_type.today()) -> TweetsOutSchema:
    return await get_tweets_func(lang=lang, stype=type, group=group, from_=from_, to_=to_)

@router.get('/get_words', response_model=TweetsOutSchema)
async def get_words(source='words', lang: str = 'Italian', min_frequency: int=-1, from_: date_type='2024-01-01', to_: date_type=date_type.today()) -> TweetsOutSchema:
    return await get_word_frequency(source=source, lang=lang, min_frequency=min_frequency, from_=from_, to_=to_)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}