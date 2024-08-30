from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import json
import requests
from ramp_model import generate_career_recommendations
from data_processing import fetch_all_jobs_data, fetch_all_major_data, preprocess_and_translate_data, save_data

app = Flask(__name__)

# 데이터 저장 폴더
UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# API 키 정의
oapi_key = 'dce42638afaf57784a701d4b5371cdef'

def load_or_update_data():
    processed_jobs_data = []
    processed_major_data = []

    # 처리된 데이터 파일 로드 시도
    try:
        with open('processed_jobs_data.json', 'r', encoding='utf-8') as f:
            processed_jobs_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Jobs data file not found or unreadable. Fetching new data...")
        jobs_data = fetch_all_jobs_data(oapi_key)
        processed_jobs_data = preprocess_and_translate_data(jobs_data, data_type='job')
        save_data(processed_jobs_data, None)  # Jobs data만 저장

    try:
        with open('processed_major_data.json', 'r', encoding='utf-8') as f:
            processed_major_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Major data file not found or unreadable. Fetching new data...")
        major_data = fetch_all_major_data(oapi_key)
        processed_major_data = preprocess_and_translate_data(major_data, data_type='major')
        save_data(None, processed_major_data)  # Major data만 저장

    return processed_jobs_data, processed_major_data

# 데이터 로드 또는 업데이트
processed_jobs_data, processed_major_data = load_or_update_data()

@app.route('/')
def index():
    files = get_file_list()
    return render_template('index.html', files=files)

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        user_input = request.form.get('user_input')

        if not user_input:
            return render_template('index.html', error="Please enter your interests.")

        recommendations = generate_career_recommendations(processed_jobs_data, processed_major_data, user_input)

        if not recommendations or "Error" in recommendations:
            print(f"Recommendations response: {recommendations}")  # 추가된 로그
            return render_template('index.html', error="Could not generate recommendations. Please try again.")

        return render_template('result.html', recommendations=recommendations)

    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # 콘솔에 오류 출력
        return render_template('index.html', error=f"Unexpected error: {str(e)}")

@app.route('/api/files')
def list_files():
    """데이터 폴더 내 엑셀 파일 목록을 반환합니다."""
    files = get_file_list()
    return jsonify(files)

@app.route('/api/data/<filename>')
def api_data(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    df = pd.read_excel(file_path, engine='openpyxl')
    data = df.to_dict(orient='records')  # 데이터를 JSON 형식으로 변환
    return jsonify(data)

def get_file_list():
    """지정된 폴더 내 엑셀 파일 목록을 가져옵니다."""
    return [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.xlsx')]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
