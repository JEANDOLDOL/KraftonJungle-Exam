import requests, random
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
from bs4 import BeautifulSoup

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbjungle

# 타겟 URL을 읽어서 HTML를 받아오고,


def insertall():
    url = 'https://www.moviechart.co.kr/rank/boxoffice'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(
        url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    # print(soup)  # HTML을 받아온 것을 확인할 수 있다.

    # select를 이용해서, li들을 불러오기
    movies = soup.select(
        '#content > div.wArea.space.title > div.listTable.group1 > table > tbody > tr')
    for movie in movies:
        # 영화이름 뽑기
        mvname = movie.select_one('.title > a').text

        # 개봉일 뽑기
        finddate = movie.select_one('.date').text
        (open_year, open_month, open_day) = [
            int(element) for element in finddate.split('.')]

        # 누적 관람객 뽑기
        mvcnt = movie.select_one('.cumulative').text
        mvcnt = mvcnt.replace(' ', '')
        mvcnt = mvcnt.replace('\r\n', '')
        mvcnt = mvcnt.replace('명', '')
        mvcnt = mvcnt.replace(',', '')
        mvcnt = int(mvcnt)

        # 영화 정보 url뽑기
        info_url = movie.select_one('.title > a')
        info_url = 'https://www.moviechart.co.kr'+info_url.attrs['href']

        # 평점을 이용하여, 좋아요수를 임의로 만든다
        likes = random.randrange(0, 100)

        # 존재하지 않는 영화인 경우만 추가한다.
        found = list(db.movies.find({'title': mvname}))
        if found:
            continue

        #포스터 추출
        url = f'http://www.cine21.com/search/?q={mvname}'
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get(
        url, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        poster_url = soup.select_one('#content > div.culm2_area > div.culm2_l > ul.mov_list > li > a > img')
        poster_url = poster_url.attrs['src']
        doc = {
            'title': mvname,
            'open_year': open_year,
            'open_month': open_month,
            'open_day': open_day,
            'viewers': mvcnt,
            'info_url': info_url,
            'poster_url': poster_url,
            'likes': likes,
            'trashed': False,
        }
        db.movies.insert_one(doc)

        print('완료: ', mvname, open_year, open_month, open_day, mvcnt, info_url, poster_url)

# def findposter() :
    #_raw9Zq_CJKuJvr0PsfeRwA4_48 > div:nth-child(1) > div > div.qlJdOe > div > div > div > div
    #_3aw9ZrLDN8Gk2roPzr-UyA0_51 > div:nth-child(1) > div > div.qlJdOe > div > div > div > div > g-img

if __name__ == '__main__':

    db.movies.drop()
    # 영화 사이트를 scraping 해서 db 에 채우기
    insertall()
