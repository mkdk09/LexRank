from flask import *
from flask_socketio import SocketIO
# analyzer.pyをimport
import analyzer
import LexRank

app = Flask(__name__)
socketio = SocketIO(app, async_mode=None)

# [削除]value_str = ""
result = []  # [変更] 結果を格納する配列
wiki_title = ""

@app.route("/")
def init():
    # value_strをhtml側で使えるようにする
    # [変更] value_str -> result
    return render_template('index.html', result=result)

#  action="/reset"
@app.route("/reset", methods=["GET", "POST"])
def reset_result():
    global result
    global wiki_title
    wiki_title = ""
    result = []
    return render_template('index.html', result=result, wiki_title=wiki_title)

#  action="/input"
@app.route("/input", methods=["GET", "POST"])
def get_form():
    global value_str
    global wiki_title
    
    # フォームの値を受け取る
    try:
        value_str = request.form['str']  # name="str"のinputタグの値を取得
    # ページ読み込み時
    except:
        value_str = ""

    # tense_analyze関数の実行
    Analyzer = analyzer.Analyzer()
    value_str, tense = Analyzer.tense_analyze(value_str)

    LR = LexRank.LexRank()
    sentences, corpus, summary = LR.tense_analyze(value_str)

    """
    # 結果をresultに追加
    appendList = []
    if(value_str):
        appendList.append(value_str)
    if(tense):
        appendList.append(tense)
    result.append(appendList)
    """

    for sentence in summary:
        result.append(sentences[corpus.index(sentence.__str__())])

    # print(sentences)
    # print(corpus)
    # print(summary)
    print(result)

    # [変更] value_str -> result
    # index.html内にて{{ result }}で挿入できる
    return render_template('index.html', result=result, wiki_title=wiki_title)

import requests,bs4
import wikipedia
#  action="/wiki"
@app.route("/wiki", methods=["GET", "POST"])
def set_wiki():
    wikipedia.set_lang("ja")
    url = "https://ja.wikipedia.org/wiki/" + wikipedia.random()
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    title = soup.find('title')
    global wiki_title
    wiki_title = title.text
    context = soup.select('.mw-parser-output > p')
    value_str = ""
    for c in context:
        value_str += c.text

    return render_template('index.html', value_str=value_str, wiki_title=wiki_title)

if __name__ == "__main__":
    # debugはデプロイ時にFalseにする
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)  # 変更


