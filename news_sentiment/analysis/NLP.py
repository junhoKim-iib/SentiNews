from keybert import KeyBERT
from konlpy.tag import Okt
from wordcloud import WordCloud, STOPWORDS
from io import BytesIO
import base64
from konlpy.corpus import kolaw

import numpy as np
import nltk
from tqdm import tqdm
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_addons as tfa
from transformers import BertTokenizer, TFBertForSequenceClassification

# import transformers

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





# 뉴스 모델과 저장할 감성 모델을 인자로 받음
# 
def news_analysis(news_model, analysis_model):
    obj_list = []
    model_path = 'best_model.h5'
    MODEL_NAME = "klue/bert-base"
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)

    bert_model = tf.keras.models.load_model(model_path, custom_objects={'TFBertForSequenceClassification': TFBertForSequenceClassification})
     
    news_list = news_model.objects.all()
    ## 테스트용
    #news_list = news_model.objects.filter(date__year='2023', date__month='3', date__day='10') # 테스트용
    #news_list = news_model.objects.all()[:10]# 뉴스 10개만 테스트

    for news in news_list:
        content = news.content # 뉴스 내용 불러오기 
        sentence_tokens = nltk.sent_tokenize(content) # 뉴스 내용을 문장 단위로 쪼개서 리스트에 저장
        sentence_tokens.extend([news.subject] * (int(len(sentence_tokens)* 0.25))) # 제목을 25%만큼 가중치를 줌
        input = convert_data(sentence_tokens) # 문장 단위로 쪼개진 뉴스 내용을 BERT 모델에 입력할 수 있도록 변환

        predicted_value = bert_model.predict(input) # 예측하기 
        predicted_label = np.argmax(predicted_value, axis=1) # 예측된 라벨
        major_sentiment = np.bincount(predicted_label).argmax() # 예측된 라벨 중 가장 많은 라벨


        if major_sentiment == 0:
            obj = analysis_model(news = news, sentiment = 0)

        elif major_sentiment == 1:
            obj = analysis_model(news = news, sentiment = 1)

        else:
            obj = analysis_model(news = news, sentiment = 2)

        obj_list.append(obj) # 뉴스와 감성을 저장할 객체 리스트에 저장

        
        # 테스트용
        print(news.subject ,obj.sentiment) 
        print(news.url)
        print(predicted_label)

    return obj_list 






def main_keywords(obj_list):
    key_model = KeyBERT('paraphrase-multilingual-MiniLM-L12-v2')

    total_title = ""
    for obj in obj_list:
        total_title += obj.subject + " "
    print(1)
    # 입력 문장 전처리
    input_text = obj.content # 최종 인풋 데이터

    # read stopwords.txt
    with open('stopwords.txt', 'r', encoding='utf-8') as f:
        stopwords = f.read().split()

    
    okt = Okt()
    input_tokens = okt.nouns(total_title)
    input_text = ' '.join(input_tokens) # 리스트를 문자열로 합치기
    keywords = key_model.extract_keywords(input_text, keyphrase_ngram_range=(1,1), top_n=20,use_maxsum=True , stop_words=stopwords)
    print(keywords)
    keywords_dict = dict(keywords)
    print(keywords_dict)
    word_cloud = WordCloud(width=2000,height=500 ,margin=10,background_color='white' ,contour_color='#d9e1e5', contour_width=2,font_path='C:/Windows/Fonts/malgun.ttf', max_words=100, max_font_size=300)
    word_cloud.generate_from_frequencies(keywords_dict)
    img = BytesIO()
    fig = plt.figure(figsize=(10,5))
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)

    img_base64 = base64.b64encode(img.getvalue()).decode()

    print("keywords: ", keywords)
  
    return img_base64



