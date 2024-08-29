from flask import Flask, render_template, send_file, jsonify
import pandas as pd
import os

app = Flask(__name__)

# 데이터 저장 폴더
UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_file_list():
    """지정된 폴더 내 엑셀 파일 목록을 가져옵니다."""
    return [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.xlsx')]

@app.route('/')
def index():
    # 엑셀 파일 목록을 가져와서 index.html로 전달
    files = get_file_list()
    return render_template('index.html', files=files)

@app.route('/data/<filename>')
def data(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return 'File not found', 404

    df = pd.read_excel(file_path, engine='openpyxl')
    return df.to_html()

if __name__ == '__main__':
    app.run(debug=True)
