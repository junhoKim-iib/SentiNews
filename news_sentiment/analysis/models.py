from django.db import models
# import for database
import psycopg2
import logging

 # import for json
import os, json
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your models here.
with open(os.path.join(BASE_DIR, 'secrets.json')) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


DB_HOST = get_secret("DB_HOST") # database host
DB_DATABASE_NEWS = get_secret("DB_DATABASE_NEWS") # news database
DB_USER = get_secret("DB_USER") # database user
DB_PASSWORD = get_secret("DB_PASSWORD") # database password


# set logging level to debug
#logging.basicConfig(level=logging.DEBUG)

def insert_stock_news(data):
    conn = psycopg2.connect(host=DB_HOST, database=DB_DATABASE_NEWS, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    for item in data:
        cur.execute("INSERT INTO stock_news (company, subject, date, summary, content, url) VALUES (%s, %s, %s, %s, %s, %s)", (item['company'] ,item['subject'], item['date'], item['summary'], item['content'], item['url']))
    conn.commit()
    cur.close()
    conn.close()


