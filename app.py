from flask import Flask, jsonify, request
from data_processing import fetch_all_jobs_data, fetch_all_major_data, preprocess_data, save_data
from ramp_model import generate_career_recommendations

# Flask 앱 생성
app = Flask(__name__)

# API 엔드포인트 정의: 기본 테스트용 라우트
@app.route('/')
def index():
    return "Welcome to the Career Recommendation API!"

# API 엔드포인트: 직업 및 학과 정보 제공
@app.route('/api/recommendations', methods=['POST'])
def career_recommendations():
    try:
        # 클라이언트로부터 사용자의 관심사 받아오기
        user_input = request.json.get('user_input')

        if not user_input:
            return jsonify({"error": "User input is required."}), 400

        # API 키 정의
        oapi_key = 'dce42638afaf57784a701d4b5371cdef'

        # 직업백과 데이터 가져오기 및 전처리
        jobs_data = fetch_all_jobs_data(oapi_key)
        processed_jobs_data = preprocess_data(jobs_data, data_type='job')

        # 학과정보 데이터 가져오기 및 전처리
        major_data = fetch_all_major_data(oapi_key)
        processed_major_data = preprocess_data(major_data, data_type='major')

        # 사용자 입력에 따른 진로 추천 생성
        recommendations = generate_career_recommendations(processed_jobs_data, processed_major_data, user_input)

        # 추천 결과를 JSON으로 반환
        return jsonify({"recommendations": recommendations})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Flask 서버 실행
    app.run(debug=True)
