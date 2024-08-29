from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    # 엑셀 파일의 경로를 지정합니다
    file_path = 'data/직업세세분류.xlsx'

    # 엑셀 파일을 읽어옵니다
    df = pd.read_excel(file_path, engine='openpyxl')

    # 데이터 프레임을 JSON으로 변환합니다
    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
