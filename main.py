from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tweets import get_tweets as get_tweets_func
from words import get_word_frequency, get_langs, check_present
from schemes import TweetsOutSchema
from datetime import date as date_type
from datetime import datetime
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'https://www.xresearch.it'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
first_day = datetime.strptime('2024-01-06', '%Y-%m-%d').date()

@app.get('/get_tweets', response_model=TweetsOutSchema)
async def get_tweets(lang: str = '', type: str = '', group: str='week', from_: date_type=first_day, to_: date_type=date_type.today(), pivot: bool=False) -> TweetsOutSchema:
    return await get_tweets_func(lang=lang, stype=type, group=group, from_=from_, to_=to_, pivot=pivot)

@app.get('/get_words', response_model=TweetsOutSchema)
async def get_words(source: str='words', lang: str = 'Italian', min_frequency: int=-1, from_: date_type=first_day, to_: date_type=date_type.today(), filter_type: str='tf_idf', aggregate: bool=True, pivot: bool=False) -> TweetsOutSchema:
    return await get_word_frequency(source=source, lang=lang, min_frequency=min_frequency, from_=from_, to_=to_, filter_type=filter_type, aggregate=aggregate, pivot=pivot)

@app.get('/get_langs_words')
async def get_langs_words(source: str='words'):
    return await get_langs(source=source)

@app.get('/check_words_presence', response_model=bool)
async def get_langs_words(source: str='words', lang: str = 'Italian', min_frequency: int=-1, from_: date_type=first_day, to_: date_type=date_type.today(), filter_type: str='tf_idf') -> bool:
    return await check_present(source=source, from_=from_, to_=to_, lang=lang, min_frequency=min_frequency, filter_type=filter_type)