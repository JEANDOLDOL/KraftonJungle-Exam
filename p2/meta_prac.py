import requests
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
from bs4 import BeautifulSoup

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbjungle   

# 타겟 URL을 읽어서 HTML를 받아오고,


def insertall() :

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(
        'https://www.moviechart.co.kr/info/movieinfo/detail/20228797', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    # print(soup)  # HTML을 받아온 것을 확인할 수 있다.


    a = soup.select_one('#content > div.info > div > div.movieIner > div.poster > a > img')
    print(a)