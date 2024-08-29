import json
from openai import OpenAI
from data_processing import preprocess_and_translate_data  # Corrected function name

client = OpenAI(
    base_url='http://localhost:11434/v1',  # Ollama API 서버 URL
    api_key='ollama',  # 실제로 필요한 경우 올바른 API 키로 설정해야 함
)

def generate_career_recommendations(processed_jobs_data, processed_major_data, user_input):
    recommendation_prompt = (
        f"User's interests are as follows: {user_input}. "
        f"The provided job data is: {json.dumps(processed_jobs_data)}. "
        f"The provided major data is: {json.dumps(processed_major_data)}. "
        "Please Based on the user's input and data, please advise the user on his or her career path long and specifically. "
    )
    
    try:
        response = client.chat.completions.create(
            model='llama3.1',
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": recommendation_prompt}
            ]
        )
        
        # 확인을 위한 상세한 로그 추가
        print(f"API Request: {recommendation_prompt}")
        print(f"API Response: {response}")

        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content
        else:
            return "No recommendations generated."
    
    except Exception as e:
        # 발생한 예외를 포함한 에러 메시지 출력
        print(f"Error generating career recommendations: {e}")
        return f"Error generating recommendations: {e}"  # 오류 메시지에 예외 세부 사항 추가