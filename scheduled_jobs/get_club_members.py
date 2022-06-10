from decouple import config
from datetime import datetime
import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

API_TOKEN = config('API_TOKEN')
DATABASE_URL = config('DATABASE_URL')
CLUB_ID = config('CLUB_ID')
DEV_ENV = config('DEV_ENV',default="no")

if DEV_ENV == "yes":
    URI = DATABASE_URL
else:
    URI = DATABASE_URL[:8] + 'ql' + DATABASE_URL[8:]
    FIXIE_URL = config('FIXIE_URL')



date = datetime.utcnow()

if date.weekday() == 2 or DEV_ENV == "yes":

    club_tag = CLUB_ID
    if DEV_ENV == "no":
            proxies = {
               'http'  : os.environ.get('FIXIE_URL', ''),
               'https' : os.environ.get('FIXIE_URL', ''),
            }
    headers = {
        'Authorization' : f'Bearer {API_TOKEN}',
    }
    if DEV_ENV == "no":
        response = requests.get(
            # the hashtag '#' is encoded as '%23' in the URL
            f'https://api.brawlstars.com/v1/clubs/%23{club_tag[1:]}/members',
            headers=headers,
            proxies=proxies,
        )
    else:
        response = requests.get(
            # the hashtag '#' is encoded as '%23' in the URL
            f'https://api.brawlstars.com/v1/clubs/%23{club_tag[1:]}/members',
            headers=headers,
        )
    club_members_list = response.json()['items']
    
    season = f'{date.year}-{date.isocalendar().week}'
    club_members_df = pd.DataFrame(
        {
            'season' : [season] * len(club_members_list),
            'player_tag' : [member['tag'] for member in club_members_list],
            'player_name' : [member['name'] for member in club_members_list],
            'trophies' : [member['trophies'] for member in club_members_list],
        },
    )
    
    engine = create_engine(URI, poolclass=NullPool)
    with engine.connect() as connection:
        club_members_df.to_sql(
            'club_members',
            connection,
            if_exists='append',
            index=False
        )
        connection.execute(
            f''' INSERT INTO job_log (job_timestamp, job)
                 VALUES('{date}', 'get_club_members.py'); '''
        )

    print('Script get_club_members.py executed successfully.')

else:
    print('Today is not Wednesday.')
