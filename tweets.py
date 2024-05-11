from models import Tweets
from schemes import TweetsOutSchema
import pandas as pd
import os
from fastapi import Response


base_path = os.path.dirname(__file__)

async def get_tweets(lang, stype, group, from_, to_) -> TweetsOutSchema:
    if not os.path.exists(f'{base_path}/data/tweets_reparsed.json'):
        data = pd.read_json(f'{base_path}/data/tweets.json', orient='records')
        melted_df = pd.melt(data, id_vars=['index', 'created_at', 'lang'], var_name='sentiment', value_name='value')
        melted_df.to_json(f'{base_path}/data/tweets_reparsed.json', orient='records')
        data = melted_df
    else:
        data = pd.read_json(f'{base_path}/data/tweets_reparsed.json', orient='records')
        
    if stype == '':
        data = data[data['sentiment'] == 'total']
    elif stype == 'all':
        data = data[data['sentiment'] != 'total']
    else: 
        data = data[data['sentiment'] == stype]       

    if lang == '':
        data = data[data['lang'] == 'all']
    elif lang == 'all':
        data = data[data['lang'] != lang]
        data = data[data['lang'] != 'zxx']
        countings = data.groupby('lang').count().reset_index()[['lang', 'value']]
        countings = countings[countings['value']>=countings['value'].quantile(0.85)]
        data = data[data['lang'].isin(countings['lang'])]
    else:
        data = data[data['lang'] == lang] 
        
 
    if group == 'week':
        data = data.groupby(['lang', 'sentiment']).resample('W-Mon', on='created_at').sum(numeric_only=True).reset_index().sort_values(by='created_at')
        data['index'] = data.index
    if group == 'month':
        data = data.groupby(['lang', 'sentiment']).resample('ME', on='created_at').sum(numeric_only=True).reset_index().sort_values(by='created_at')
        data['index'] = data.index
        
    data['created_at'] = data['created_at'].dt.date
        
    data = data[data['created_at']>=from_]
    data = data[data['created_at']<=to_]
    return Response(data.to_json(orient="records"), media_type="application/json")