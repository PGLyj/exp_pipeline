import pandas as pd
from django.conf import settings
from sqlalchemy import create_engine
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

db_name   = settings.DATABASES['default']['NAME']
db_url    = 'sqlite:////%s'%db_name
engine    = create_engine(db_url, echo=False)
df_django = pd.read_csv('csv_exp.csv', sep = ',')
df_django.to_sql('exp_data', engine, if_exists = 'replace', index=False)