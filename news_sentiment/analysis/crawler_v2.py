import datetime

start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 12, 31)
delta = datetime.timedelta(days=1)
dates = [str(start_date + i*delta).replace('-', '') for i in range((end_date - start_date).days + 1)]


import requests
from bs4 import BeautifulSoup
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

def get_main_news(date):
    # 날짜 설정
    # date format should be: 'yyyy-mm-dd'
    # 크롤링할 URL 설정
    url = f'https://finance.naver.com/news/mainnews.naver?date={date}'
    # User-Agent 설정
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    # 페이지 요청
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(res.text, 'html.parser')
    #print(soup)
    # 뉴스 기사 리스트 추출
    news_list = soup.select('dd.articleSubject')
    # 뉴스 기사 크롤링

    return news_list



def get_news(date, news_list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    data = []
    for news in news_list:
        # 뉴스 제목 추출
        title = news.select_one('a').text

        # 뉴스 링크 추출
        link = news.select_one('a')['href']
        link = "https://finance.naver.com" + link 
        # 뉴스 내용 추출
        content_res = requests.get(link, headers=headers)
        content_res.raise_for_status()
        content_soup = BeautifulSoup(content_res.text, 'html.parser')
        content = content_soup.select_one('div#content').text.strip()
        
        item = {'subject': title, 'url': link, 'content': content, 'date': date}
        # 결과 출력
        data.append(item)

    return data


def main():
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_main_news, date) for date in dates]
        news_lists = [future.result() for future in futures]
        futures = [executor.submit(get_news, date, news_list) for date, news_list in zip(dates, news_lists)]
        results = [future.result() for future in futures]
        print(results)
        


if __name__ == '__main__':
    main()
