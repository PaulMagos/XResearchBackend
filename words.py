from models import Words
from schemes import WordsOutSchema
import pandas as pd
import os
from fastapi import Response


base_path = os.path.dirname(__file__)

async def get_word_frequency(source, lang, min_frequency, from_, to_, filter_type) -> WordsOutSchema:
    data = pd.read_json(f'{base_path}/data/{source}.json', orient='records')
        
        
    data['created_at'] = data['created_at'].dt.date
    data = data[data['created_at']>=from_]
    data = data[data['created_at']<=to_]
        
    data = data[data['lang'] == lang] 
        
    if source == 'hashtags':
        data['word'] = data['hashtag']
        data.drop(columns='hashtag', inplace=True)
        
    if from_ != to_:
        data = data.groupby(['word', 'lang']).sum(numeric_only=True).reset_index()
        
    if min_frequency==-1:
        data = data[data['frequency']>=data['frequency'].quantile(0.95)]
    else: 
        data = data[data['frequency']>=min_frequency]
    return Response(data.to_json(orient="records"), media_type="application/json")

async def get_langs(source):
    data = pd.read_json(f'{base_path}/data/{source}.json', orient='records')
    return data['lang'].unique().tolist()

async def check_present(source, from_, to_, lang, min_frequency, filter_type):
    if not os.path.exists(f'{base_path}/data/{source}.json'):
        return False
    data = pd.read_json(f'{base_path}/data/{source}.json', orient='records')
        
    data['created_at'] = data['created_at'].dt.date
    data = data[data['created_at']>=from_]
    data = data[data['created_at']<=to_]
        
    data = data[data['lang'] == lang] 
        
    if source == 'hashtags':
        data['word'] = data['hashtag']
        data.drop(columns='hashtag', inplace=True)
        
    if from_ != to_:
        data = data.groupby(['word', 'lang']).sum(numeric_only=True).reset_index()
        
    if min_frequency==-1:
        data = data[data['frequency']>=data['frequency'].quantile(0.95)]
    else: 
        data = data[data['frequency']>=min_frequency]
        
    res = data
    if len(res) > 0:
        return True
    return False