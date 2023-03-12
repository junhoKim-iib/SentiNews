from io import BytesIO
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

def extract_keywords_and_generate_wordcloud_with_bert(text, max_words=20, width=800, height=400):
    """
    BERT 모델을 활용하여 한국어 뉴스의 핵심 키워드를 추출하고 워드클라우드를 생성
    
    :param text: str, 한국어 뉴스 기사
    :param max_words: int, 워드클라우드에 포함할 최대 단어 수
    :param width: int, 워드클라우드 이미지의 가로 크기
    :param height: int, 워드클라우드 이미지의 세로 크기
    :return: None
    """
    module_url = "https://tfhub.dev/tensorflow/bert_kor_base/1"
    bert_layer = hub.KerasLayer(module_url, trainable=True)

    def get_keyword_indices(text):
        input_tokens = ["[CLS]"] + tokenizer.tokenize(text) + ["[SEP]"]
        input_ids = tokenizer.convert_tokens_to_ids(input_tokens)
        input_mask = [1] * len(input_ids)
        segment_ids = [0] * len(input_ids)

        input_ids = pad_sequences([input_ids], maxlen=128, dtype="long", value=0, padding="post")
        input_mask = pad_sequences([input_mask], maxlen=128, dtype="long", value=0, padding="post")
        segment_ids = pad_sequences([segment_ids], maxlen=128, dtype="long", value=0, padding="post")

        outputs = bert_layer([input_ids, input_mask, segment_ids])
        sequence_output, pooled_output = outputs["sequence_output"], outputs["pooled_output"]

        values, indices = tf.math.top_k(pooled_output[0], k=max_words)

        return indices.numpy()



    tokenizer = Tokenizer()
    tokenizer.fit_on_texts([text])
    keyword_indices = get_keyword_indices(text)
    keywords = tokenizer.sequences_to_texts([keyword_indices])[0].split()

    wordcloud_text = ' '.join(keywords)
    wordcloud = WordCloud(
        font_path='NanumBarunGothic.ttf', 
        background_color='white', 
        width=width, 
        height=height, 
        max_words=max_words, 
        colormap='viridis').generate(wordcloud_text)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)

    return img_data.read()