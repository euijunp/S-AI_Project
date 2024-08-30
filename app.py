from flask import Flask, render_template, request
import json
from ramp_model import generate_career_recommendations
from data_processing import fetch_all_jobs_data, fetch_all_major_data, preprocess_and_translate_data, save_data
import os

app = Flask(__name__)

# API 키 정의 (환경 변수에서 불러오기)
oapi_key = os.getenv('OLLAMA_API_KEY', 'dce42638afaf57784a701d4b5371cdef')  # 환경 변수에서 API 키를 가져오고, 없으면 기본값 사용

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
    return render_template('index.html')

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

if __name__ == '__main__':
    # 서버를 외부에서 접근할 수 있도록 호스트와 포트를 설정
    app.run(host='0.0.0.0', port=5000, debug=True)  # 모든 IP에서 접근 가능
