# app.py
from flask import Flask, render_template, request
import json
from ramp_model import generate_career_recommendations
from data_processing import fetch_all_jobs_data, fetch_all_major_data, preprocess_and_translate_data, save_data

app = Flask(__name__)

# API 키 정의
oapi_key = 'dce42638afaf57784a701d4b5371cdef'

def load_or_update_data():
    # 데이터 로드 또는 업데이트
    try:
        with open('processed_jobs_data.json', 'r', encoding='utf-8') as f:
            processed_jobs_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        processed_jobs_data = []
        print("Jobs data file not found or unreadable. Fetching new data...")
        jobs_data = fetch_all_jobs_data(oapi_key)
        processed_jobs_data = preprocess_and_translate_data(jobs_data, data_type='job')
        save_data(processed_jobs_data, None)  # Save jobs data only

    try:
        with open('processed_major_data.json', 'r', encoding='utf-8') as f:
            processed_major_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        processed_major_data = []
        print("Major data file not found or unreadable. Fetching new data...")
        major_data = fetch_all_major_data(oapi_key)
        processed_major_data = preprocess_and_translate_data(major_data, data_type='major')
        save_data(None, processed_major_data)  # Save major data only

    return processed_jobs_data, processed_major_data

# 데이터 로드 또는 업데이트
processed_jobs_data, processed_major_data = load_or_update_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # 사용자로부터 입력 받기
        user_input = request.form.get('user_input')

        if not user_input:
            return render_template('index.html', error="Please enter your interests.")

        # 진로 추천 생성
        recommendations = generate_career_recommendations(processed_jobs_data, processed_major_data, user_input)

        if not recommendations or "Error" in recommendations:
            return render_template('index.html', error="Could not generate recommendations. Please try again.")

        return render_template('result.html', recommendations=recommendations)

    except Exception as e:
        return render_template('index.html', error=f"Unexpected error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)