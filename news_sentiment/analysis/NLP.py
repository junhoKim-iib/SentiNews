from .models import StockNews, MainNews
import torch
from transformers import BertTokenizer
from django.shortcuts import render
from .models import StockNews, MainNews

model_path = 'news_sentiment\\best_model.h5'
MODEL_NAME = "klue/bert-base"
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)

model = torch.load(model_path)

news_list = MainNews.objects.all()


negative_news = []
positive_news = []
neutral_news = []

for news in news_list:
    text = news.subject + ' ' + news.content
    inputs = tokenizer.encode_plus(text, add_special_tokens=True, return_tensors='pt')
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']
    # BERT 모델을 이용하여 분류합니다.
    with torch.no_grad():
        outputs = model(input_ids, attention_mask)
        logits = outputs[0]
        pred = torch.argmax(logits).item()
    # 결과를 results 리스트에 추가합니다.
    if pred == 0:
        neutral_news.append({'news': news, 'label': 'neutral'})
    elif pred == 1:
        positive_news.append({'news': news, 'label': 'positive'})
    else:
        negative_news.append({'news': news, 'label': 'negative'})

