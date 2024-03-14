import os
import csv
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_sentiment.settings')
django.setup()


from django.db import transaction
from analysis.models import insert_main_news


dataset_folder = 'dataset/2024-01'


@transaction.atomic
def csv_to_db(file_path):
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        insert_main_news(list(csv_reader))


def main():
    for file_name in os.listdir(dataset_folder):
        if file_name.endswith('.csv'):
            file_path = os.path.join(dataset_folder, file_name)
            csv_to_db(file_path)


if __name__ == '__main__':
    main()

