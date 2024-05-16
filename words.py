from models import Words
from schemes import WordsOutSchema
import pandas as pd
import os
from fastapi import Response
import numpy as np

base_path = os.path.dirname(__file__)

async def get_word_frequency(source, lang, min_frequency, from_, to_, filter_type, aggregate, pivot) -> WordsOutSchema:
    data = pd.read_json(f'{base_path}/data/{source}.json', orient='records')
        
    data = data[data['lang'] == lang] 
        
    if source == 'hashtags':
        data['word'] = data['hashtag']
        data.drop(columns='hashtag', inplace=True)
        
    if filter_type == 'tf_idf':
            data = tf_idf(data)
    
    data['created_at'] = data['created_at'].dt.date
    data = data[data['created_at']>=from_]
    data = data[data['created_at']<=to_]
    
        
    if from_ != to_ and aggregate:
        data = data.groupby(['word', 'lang']).sum(numeric_only=True).reset_index()
                
    if min_frequency==-1:
        data = data[data['frequency']>=data['frequency'].quantile(0.95)]
    else: 
        data = data[data['frequency']>=min_frequency]
        
    if pivot:
        # Pivot the DataFrame
        data = data.pivot_table(index='created_at', columns='word', values='frequency', fill_value=0).reset_index()
        # Rename the columns to match the desired format
        data.columns.name = None
        data[data.columns[1:]] = data[data.columns[1:]].astype('int64')
        return Response(data.to_csv(index=False), media_type='text/csv"')
        
    return Response(data.to_json(orient="records"), media_type="application/json")

async def get_langs(source):
    data = pd.read_json(f'{base_path}/data/{source}.json', orient='records')
    return data['lang'].unique().tolist()

async def check_present(source, from_, to_, lang, min_frequency, filter_type):
    if not os.path.exists(f'{base_path}/data/{source}.json'):
        return False
    data = pd.read_json(f'{base_path}/data/{source}.json', orient='records')
        
    data = data[data['lang'] == lang] 
        
    if source == 'hashtags':
        data['word'] = data['hashtag']
        data.drop(columns='hashtag', inplace=True)
        
    if filter_type == 'tf_idf':
        data = tf_idf(data)
            
    data['created_at'] = data['created_at'].dt.date
    data = data[data['created_at']>=from_]
    data = data[data['created_at']<=to_]
        
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

def tf_idf(data):
    original_data = data
    original_data['doc_freq'] = original_data.groupby('word')['word'].transform('count')
    total = original_data['doc_freq'].sum()
    total_words_per_day = original_data.groupby('created_at')['frequency'].transform('sum')
    
    original_data['tf_idf'] = (original_data['frequency']/total_words_per_day) * (np.log(total)/original_data['doc_freq'])
    original_data.drop(columns=['doc_freq'], inplace=True)    
    
    original_data = original_data[original_data['tf_idf']>0.01][original_data.columns[:-1]]
    
    return original_data