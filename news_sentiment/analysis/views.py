from django.shortcuts import render
from .models import StockNews, MainNews
from django.core.paginator import Paginator # 페이지네이션을 위한 장고 내장 모듈
# Create your views here.

# import for bert model
# import tensorflow as tf
# from transformers import BertTokenizer, TFBertForSequenceClassification

# def home(request): 
#     main_news = MainNews.objects.all()
#     context = {'main_news': main_news}
#     return render(request, 'analysis/home.html', context)



def home(request):
    news_list = MainNews.objects.all()
    paginator = Paginator(news_list, 10) # 10개의 뉴스를 한 페이지에 보여줍니다.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'analysis/home.html', context)



def stocks(request):
    return render(request, 'analysis/stocks.html', {})




# import os
# import pandas as pd
# import numpy as np
# import re
# from tqdm import tqdm
# import urllib.request
# import seaborn as sns
# import matplotlib.pyplot as plt
# import tensorflow_addons as tfa
# import tensorflow as tf
# from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
# from transformers import BertTokenizer, TFBertForSequenceClassification
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, \
#                             roc_auc_score, confusion_matrix, classification_report, \
#                             matthews_corrcoef, cohen_kappa_score, log_loss



# MODEL_NAME = "klue/bert-base"
# # model = TFBertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=3, from_pt=True)
# tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
# MAX_SEQ_LEN = 64 # 수정 블가. 수정 시 모델 재학습 필요 (학습 데이터에 대한 최대 길이)

# def convert_data(X_data):
#     # BERT 입력으로 들어가는 token, mask, segment
#     tokens, masks, segments = [], [], []
    
#     for X in tqdm(X_data):
#         # token: 입력 문장 토큰화
#         token = tokenizer.encode(X, truncation = True, padding = 'max_length', max_length = MAX_SEQ_LEN)
        
#         # Mask: 토큰화한 문장 내 패딩이 아닌 경우 1, 패딩인 경우 0으로 초기화
#         num_zeros = token.count(0)
#         mask = [1] * (MAX_SEQ_LEN - num_zeros) + [0] * num_zeros
        
#         ### 이부분 수정해야함. 제목을 입력 데이터로 할까? 아니면 내용을 입력 데이터로 할까?
#         # 해결 : 내용과 제목을 합쳐서 입력 데이터로 사용하되 제목의 가중치를 20%로 줌
#         #        뉴스 리스트 전체를 예측하는 게 아니라 뉴스 내용을 문장 단위로 쪼개서 예측하고
#         #        그 결과를 뉴스 제목과 합쳐서 예측하는 방식으로 변경
#         # segment: 문장 전후관계 구분: 오직 한 문장이므로 모두 0으로 초기화
#         segment = [0]*MAX_SEQ_LEN

#         tokens.append(token)
#         masks.append(mask)
#         segments.append(segment)


#     # numpy array로 저장
#     tokens = np.array(tokens)
#     masks = np.array(masks)
#     segments = np.array(segments)


#     return [tokens, masks, segments]




# def main_news_analysis():

#     model_path = 'best_model.h5'
#     MODEL_NAME = "klue/bert-base"
#     tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)

#     model = tf.keras.models.load_model(model_path, custom_objects={'TFBertForSequenceClassification': TFBertForSequenceClassification})
     

#     news_list = MainNews.objects.all()

#     negative_news = []
#     positive_news = []
#     neutral_news = []

#     for news in news_list:
#         title_input = convert_data(news.subject)
#         content = news.centent
#         content_split_by_sentence = content.split('.')
#         input = convert_data(content_split_by_sentence) # 뉴스 본문 문장들을 입력 데이터로 변환

#         input.extend([title_input] * int(len(content_split_by_sentence) * 0.2)) # 제목 문장 추가. 제목의 가중치는 20%
#         predicted_value = model.predict(input)

#         major_sentiment = np.argmax(predicted_value) # 예측된 감성 중 가장 큰 값을 가진 인덱스를 가져옴

#         if major_sentiment == 0:
#             neutral_news.append({'news': news, 'label': 'neutral'})

#         elif major_sentiment == 1:
#             positive_news.append({'news': news, 'label': 'positive'})

#         else:
#             negative_news.append({'news': news, 'label': 'negative'})


#     return negative_news, positive_news, neutral_news




