import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_sentiment.settings')
django.setup()

from analysis.NLP import news_analysis

def main():
    news_analysis()


if __name__ == '__main__':
    main()


