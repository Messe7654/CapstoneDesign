from flask import Flask, render_template

app = Flask(__name__)

# 페이지 추가시 이 부분을 새로 추가해야한다.
@app.route('/') # 접속하려는 URL을 입력으로
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)