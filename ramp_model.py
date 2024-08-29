import json
from openai import OpenAI
from data_processing import fetch_all_jobs_data, fetch_all_major_data, preprocess_data

# OpenAI 클라이언트 설정
client = OpenAI(
    base_url='http://localhost:11434/v1',  # Ollama API 서버 URL
    api_key='ramp',  # Ollama API 키 (실질적으로 사용 안 함.)
)

def generate_career_recommendations(processed_jobs_data, processed_major_data, user_input):
    # 추천 프롬프트 생성
    recommendation_prompt = (
        f"User's interests: {user_input}. "
        f"Here are some available job and major data: Jobs: {json.dumps(processed_jobs_data[:5])}. Majors: {json.dumps(processed_major_data[:5])}. "
        "Based on this information, please suggest potential career paths and related majors that align with the user's interests."
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
        
        # 추천 결과 반환
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Error generating career recommendations: {e}")
        return None
