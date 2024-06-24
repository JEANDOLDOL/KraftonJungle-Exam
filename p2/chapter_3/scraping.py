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
        'https://www.moviechart.co.kr/rank/boxoffice', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    # print(soup)  # HTML을 받아온 것을 확인할 수 있다.


    # select를 이용해서, li들을 불러오기
    movies = soup.select(
        '#content > div.wArea.space.title > div.listTable.group1 > table > tbody > tr')
    for movie in movies:
        mvname = movie.select_one('.title > a').text

        finddate = movie.select_one('.date').text
        (open_year, open_month, open_day) = [
        int(element) for element in finddate.split('.')]

        mvcnt = movie.select_one('.cumulative').text
        mvcnt = mvcnt.replace(' ', '')
        mvcnt = mvcnt.replace('\r\n', '')
        
        doc = {
            'title' : mvname,
            'open_year' : open_year,
            'open_month' : open_month,
            'open_day' : open_day,
            'viewers' : mvcnt 
        }
        db.movies.insert_one(doc)
        
        print('완료: ', mvname, open_year, open_month, open_day, mvcnt)
if __name__ == '__main__':
    
    db.movies.drop()
    # 영화 사이트를 scraping 해서 db 에 채우기
    insertall()
db.movies.update_one({'title':'범죄도시4'},{'$set':{'open_year':'1992'}})

