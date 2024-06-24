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
    title_receive.replace(' ','\u00A0')
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
    # 모든 document 찾기 ({'_id':False} 이부분을 추가하지 않으면 에러뜸 왜지..?)
    table = list(db.memos.find({}).sort({'like':-1}))
    for i in table:
        i['_id'] = str(i['_id'])
    return jsonify({'result': 'success', 'articles': table})

#좋아요 기능 생성
@app.route('/memos/like', methods=['POST'])
def like_article():
    #클라이언트로부터 title 받기.
    title_receive = request.form['title_give']
    article = db.memos.find_one({'title':title_receive})
    
    #받은 title에 해당하는 like +1
    new_like = article['like'] + 1
    
    #몽고db에 업데이트
    result = db.memos.update_one({'title':title_receive}, {'$set': {'like': new_like}})

    return jsonify({'result': 'success', 'msg': '좋아요 완료!'})

#수정할 title,content를 db에 업데이트
@app.route('/memos/edit', methods=['POST'])
def edit_articles():
    #클라이언트로부터 수정된 title,content 받고 업데이트.
    title_receive = request.form['title_give']
    original_id = request.form['ori_id']
    db.memos.update_one({'_id':original_id}, {'$set': {'title': title_receive}})
    content_receive = request.form['content_give']
    db.memos.update_one({'_id':original_id}, {'$set': {'content': content_receive}})
    print(title_receive,content_receive,original_id)
    return jsonify({'result': 'success', 'msg': '수정 완료!'})

#해당 도큐멘트를 제거
@app.route('/memos/discard', methods=['POST'])
def discard_article():
    #클라이언트로부터 삭제할 title을 받음.
    title_receive = request.form['title_give']
    #해당 title에 해당하는 도큐먼트 삭제.
    db.memos.delete_one({'title':title_receive})

    return jsonify({'result': 'success', 'msg': '삭제 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
    # ,{'_id':False}