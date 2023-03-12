import os
import pandas as pd
import numpy as np
import nltk
import re
from tqdm import tqdm
import urllib.request
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow_addons as tfa
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from transformers import BertTokenizer, TFBertForSequenceClassification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, \
                            roc_auc_score, confusion_matrix, classification_report, \
                            matthews_corrcoef, cohen_kappa_score, log_loss



# X_data 는 뉴스 내용을 문장 단위로 쪼개서 저장한 문자열 리스트
def convert_data(X_data):
    
    MODEL_NAME = "klue/bert-base"
    # model = TFBertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=3, from_pt=True)
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
    MAX_SEQ_LEN = 64 # 수정 블가. 수정 시 모델 재학습 필요 (학습 데이터에 대한 최대 길이)


    # BERT 입력으로 들어가는 token, mask, segment
    tokens, masks, segments = [], [], []
    
    for X in tqdm(X_data):
        # token: 입력 문장 토큰화
        token = tokenizer.encode(X, truncation = True, padding = 'max_length', max_length = MAX_SEQ_LEN)
        
        # Mask: 토큰화한 문장 내 패딩이 아닌 경우 1, 패딩인 경우 0으로 초기화
        num_zeros = token.count(0)
        mask = [1] * (MAX_SEQ_LEN - num_zeros) + [0] * num_zeros
        
        ### 이부분 수정해야함. 제목을 입력 데이터로 할까? 아니면 내용을 입력 데이터로 할까?
        # 해결 : 내용과 제목을 합쳐서 입력 데이터로 사용하되 제목의 가중치를 20%로 줌
        #        뉴스 리스트 전체를 예측하는 게 아니라 뉴스 내용을 문장 단위로 쪼개서 예측하고
        #        그 결과를 뉴스 제목과 합쳐서 예측하는 방식으로 변경
        # segment: 문장 전후관계 구분: 오직 한 문장이므로 모두 0으로 초기화
        segment = [0]*MAX_SEQ_LEN

        tokens.append(token)
        masks.append(mask)
        segments.append(segment)


    # numpy array로 저장
    tokens = np.array(tokens)
    masks = np.array(masks)
    segments = np.array(segments)


    return [tokens, masks, segments]




def news_analysis(news_model, analysis_model):
    obj_list = []
    model_path = 'best_model.h5'
    MODEL_NAME = "klue/bert-base"
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)

    bert_model = tf.keras.models.load_model(model_path, custom_objects={'TFBertForSequenceClassification': TFBertForSequenceClassification})
     
    #news_list = db_model.objects.all()
    #news_list = news_model.objects.filter(date__year='2023')
    news_list = news_model.objects.all()[:10]

    for news in news_list:
        content = news.content
        sentence_tokens = nltk.sent_tokenize(content)
        sentence_tokens.extend([news.subject] * (int(len(sentence_tokens)* 0.15)))
        input = convert_data(sentence_tokens)

        #input.extend([title_input] * int(len(content_split_by_sentence) * 0.2)) # 제목 문장 추가. 제목의 가중치는 20%
        predicted_value = bert_model.predict(input)
        predicted_label = np.argmax(predicted_value, axis=1) # 예측된 라벨
        major_sentiment = np.bincount(predicted_label).argmax() # 예측된 라벨 중 가장 많은 라벨
        if major_sentiment == 0:
            obj = analysis_model(news = news, sentiment = 0)

        elif major_sentiment == 1:
            obj = analysis_model(news = news, sentiment = 1)

        else:
            obj = analysis_model(news = news, sentiment = 2)

        obj_list.append(obj)

        print(news.subject ,obj.sentiment)
        print(news.url)
        print(predicted_label)

    return obj_list



# test
