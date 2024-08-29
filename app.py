# app.py
from flask import Flask, render_template, request
import json
from ramp_model import generate_career_recommendations

app = Flask(__name__)

# 미리 처리된 데이터를 로드
try:
    with open('processed_jobs_data.json', 'r', encoding='utf-8') as f:
        processed_jobs_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    processed_jobs_data = []
    print(f"Error loading jobs data: {e}")

try:
    with open('processed_major_data.json', 'r', encoding='utf-8') as f:
        processed_major_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    processed_major_data = []
    print(f"Error loading major data: {e}")

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