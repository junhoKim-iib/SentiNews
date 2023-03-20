## News Sensitivity Analysis Django Web project

### Description
금융 뉴스 감성 분석 웹 시각화 프로젝트

### 📜 **서비스 내용**

금융 뉴스를 크롤링해서 긍정/부정/중립으로 분류해 시각적으로 보여주는 서비스입니다. 

#### 핵심 기능 

1. 긍정적인 뉴스와 부정적인 뉴스 리스트 제공
2. 분류된 감성비율을 파이차트로 제공
3. 핵심 키워드를 워드클라우드로 시각화
4. 종목별 뉴스 감성 분석

### 🔨**사용 기술**

- Django, Postgresql
- Bootstrap, Git

### 🖥 개발 내용

1. **뉴스 수집**
    
    수집에는 beautifulSoup 라이브러리를 사용했습니다. 수집 URL은 아래와 같습니다. 
    
    주요 뉴스: [https://finance.naver.com/news/mainnews.naver](https://finance.naver.com/news/mainnews.naver) 
    
    종목별 뉴스: [https://finance.naver.com/news/news_search.naver](https://finance.naver.com/news/news_search.naver)
    
2. **감성 분류 모델**
    
    감성 분류를 위해 BERT 모델을 사용했습니다. 
    
    학습 데이터셋과 모델은 [https://github.com/ukairia777/finance_sentiment_corpus](https://github.com/ukairia777/finance_sentiment_corpus) 를 참고했습니다. 
    
    뉴스 본문을 문장 단위로 나누어 분류를 진행합니다. 본문의 문장들에서 가장 많이 나온 감성을 라벨링합니다.
    

1. **wordcloud 생성**
    
    사용자가 기간을 설정해서 검색하면, 해당 기간 동안의 주요 키워드를 **wordcloud**로 보여줍니다. 
    
    기간을 설정하지 않을 경우 최근 일주일 동안의 주요 키워드를 출력합니다. 
    
2. **Django framework**
    
    MVT 패턴을 기반으로 Django와 BootStrap으로 웹을 구현했습니다. 
    
    로그인/회원가입 기능, 기간 필터 기능, 종목 검색 기능을 사용할 수 있습니다. 
    
    메인 페이지에는 긍정/부정 뉴스리스트, 파이차트, 워드클라우드를 보여줍니다. 
    


### 👀 서비스 화면

<img src="https://user-images.githubusercontent.com/59608767/225847158-244c93fa-dae3-47bf-b7bf-277dd5a6332a.png" width="700"/>
