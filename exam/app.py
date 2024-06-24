from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)


client = MongoClient('localhost', 27017)
db = client.dbjungle

@app.route('/')
def home():
    return render_template('index.html')

#입력받은 정보로 부터 db생성
@app.route('/memos', methods=['POST'])
def save_article():
    #클라이언트로부터 제목과 내용 받기.
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    
    #받은 데이터로 db에 들어갈 article 만들기
    article = {
        'title' : title_receive,
        'content' : content_receive,
        'like' : 0
    }
    
    #몽고db에 저장
    db.memos.insert_one(article)

    return jsonify({'result': 'success', 'msg': '포스팅 성공!'})

#db에서 articles 추출
@app.route('/memos', methods=['GET'])
def show_articles():
    # 모든 document 찾기
    table = list(db.memos.find({},{'_id':False}))
    return jsonify({'result': 'success', 'articles': table})

#좋아요 기능 생성
@app.route('/memos/like', methods=['POST'])
def like_article():
    #클라이언트로부터 title 받기.
    title_receive = request.form['title_give']
    
    #받은 title에 해당하는 like 표시
    
    
    #받은 title에 해당하는 like +1
    
    
    #몽고db에 저장
    db.memos.insert_one(article)

    return jsonify({'result': 'success', 'msg': '포스팅 성공!'})
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)