from flask import Flask, render_template, request, jsonify
import json
from ramp_model import generate_career_recommendations

app = Flask(__name__)

# 미리 처리된 데이터를 로드
with open('processed_jobs_data.json', 'r', encoding='utf-8') as f:
    processed_jobs_data = json.load(f)

with open('processed_major_data.json', 'r', encoding='utf-8') as f:
    processed_major_data = json.load(f)

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

        return render_template('result.html', recommendations=recommendations)

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
