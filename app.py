from flask import Flask, render_template, request, jsonify
from data_processing import fetch_all_jobs_data, fetch_all_major_data, preprocess_data
from ramp_model import generate_career_recommendations

app = Flask(__name__)

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

        # API 키 정의
        oapi_key = 'dce42638afaf57784a701d4b5371cdef'

        # 직업 및 학과 정보 가져오기 및 전처리
        jobs_data = fetch_all_jobs_data(oapi_key)
        processed_jobs_data = preprocess_data(jobs_data, data_type='job')

        major_data = fetch_all_major_data(oapi_key)
        processed_major_data = preprocess_data(major_data, data_type='major')

        # 진로 추천 생성
        recommendations = generate_career_recommendations(processed_jobs_data, processed_major_data, user_input)

        return render_template('result.html', recommendations=recommendations)

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
