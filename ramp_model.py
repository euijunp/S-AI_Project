# ramp_model.py
import json
from openai import OpenAI
from data_processing import preprocess_data

# OpenAI 클라이언트 설정
client = OpenAI(
    base_url='http://localhost:11434/v1',  # Ollama API 서버 URL
    api_key='ramp',  # 실제로 필요한 경우 올바른 API 키로 설정해야 함
)

def generate_career_recommendations(processed_jobs_data, processed_major_data, user_input):
    # 추천 프롬프트 생성
    recommendation_prompt = (
        f"User's interests: {user_input}. "
        f"Here is job and major data related to the user's interests: Jobs: {json.dumps(processed_jobs_data)}. Majors: {json.dumps(processed_major_data)}. "
        "Please suggest potential career paths and related majors that align with the user's interests based on this data. "
        "If the information is insufficient or not directly related, provide helpful advice or alternative suggestions that could benefit the user."
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
        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content
        else:
            return "No recommendations generated."
    
    except Exception as e:
        print(f"Error generating career recommendations: {e}")
        return "Error generating recommendations, please try again."