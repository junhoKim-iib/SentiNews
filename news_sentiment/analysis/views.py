from django.shortcuts import render
from .models import StockNews, MainNews
from django.core.paginator import Paginator # 페이지네이션을 위한 장고 내장 모듈
# Create your views here.

# import for bert model
import torch
from transformers import BertTokenizer


# def home(request): 
#     main_news = MainNews.objects.all()
#     context = {'main_news': main_news}
#     return render(request, 'analysis/home.html', context)



# def home(request):
#     news_list = MainNews.objects.all()
#     paginator = Paginator(news_list, 10) # 10개의 뉴스를 한 페이지에 보여줍니다.
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'page_obj': page_obj
#     }
#     return render(request, 'analysis/home.html', context)



def stocks(request):
    return render(request, 'analysis/stocks.html', {})






def home(request):

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


    context = {
        'negative_news': negative_news,
        'positive_news': positive_news,
        'neutral_news': neutral_news
    }
    return render(request, 'analysis/home.html', context)





