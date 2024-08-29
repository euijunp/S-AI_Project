import json
from openai import OpenAI
from data_processing import preprocess_and_translate_data  # Corrected function name

client = OpenAI(
    base_url='http://localhost:11434/v1',  # Ollama API 서버 URL
    api_key='ollama',  # 실제로 필요한 경우 올바른 API 키로 설정해야 함
)

def generate_career_recommendations(processed_jobs_data, processed_major_data, user_input):
    recommendation_prompt = (
    f"User's profile: Interests and background: {user_input}. "
    f"Career data from CareerNet and WorkNet: {json.dumps(processed_jobs_data)}. "
    f"Major and education data from academic sources: {json.dumps(processed_major_data)}. "
    f"Certification data from Q-Net: {json.dumps(processed_certification_data)}. "
    "Based on the user's profile and the provided data, generate a personalized career recommendation. "
    "Take into account the user's interests, career prospects, relevant academic fields, and potential certifications. "
    "Ensure the recommendation is detailed and actionable, incorporating relevant job trends and requirements from CareerNet, WorkNet, and Q-Net APIs."
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