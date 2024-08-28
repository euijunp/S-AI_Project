import json
from openai import OpenAI
from data_processing import fetch_all_jobs_data, fetch_all_major_data, preprocess_data, save_data

# OpenAI 클라이언트 설정 (Ollama 서버의 URL 및 API 키)
client = OpenAI(
    base_url='http://localhost:11434/v1',  # Ollama API 서버 URL
    api_key='ramp',  # Ollama API 키 (실질적으로 사용 안 함.)
)

def generate_career_recommendations(processed_jobs_data, processed_major_data):
    # 사용자로부터 한글 입력 받기
    user_input = input("진로 추천을 위한 관심사나 정보를 한글로 입력하세요: ")

    # 데이터를 모델에 전달하여 추천 생성
    recommendation_prompt = (
        f"사용자의 관심사: {user_input}, "
        f"그리고 사용 가능한 직업 및 전공 데이터: {json.dumps(processed_jobs_data[:5])}, {json.dumps(processed_major_data[:5])}, "
        "이 정보를 바탕으로 사용자의 관심사에 맞는 잠재적인 진로 경로를 추천하고 관련 전공을 제안해 주세요."
    )
    
    try:
        # Ollama API 호출
        response = client.chat.completions.create(
            model='phi3.5',
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": recommendation_prompt}
            ]
        )
        
        # 결과 출력
        print("Generated Career Recommendations:")
        # 응답 객체
        print(response.choices[0].message.content)
    
    except Exception as e:
        print(f"Error generating career recommendations: {e}")

# 메인 실행 함수
if __name__ == "__main__":
    # API 키 정의
    oapi_key = 'dce42638afaf57784a701d4b5371cdef'

    # 직업백과 데이터 가져오기 및 전처리
    jobs_data = fetch_all_jobs_data(oapi_key)
    processed_jobs_data = preprocess_data(jobs_data, data_type='job')
    
    # 학과정보 데이터 가져오기 및 전처리
    major_data = fetch_all_major_data(oapi_key)
    processed_major_data = preprocess_data(major_data, data_type='major')
    
    # 전처리된 데이터 기반으로 Ollama 모델을 사용하여 진로 추천 생성
    generate_career_recommendations(processed_jobs_data, processed_major_data)
    
    # 데이터 저장
    save_data(processed_jobs_data, processed_major_data)
