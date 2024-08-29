import json
from openai import OpenAI
from data_processing import preprocess_and_translate_data  # Corrected function name

client = OpenAI(
    base_url='http://localhost:11434/v1',  # Ollama API 서버 URL
    api_key='',  # 실제로 필요한 경우 올바른 API 키로 설정해야 함
)

def generate_career_recommendations(processed_jobs_data, processed_major_data, 
                                     current_exam_data, national_exam_data, 
                                     qualification_categories_data, user_input):
    recommendation_prompt = (
        f"User's interests are as follows: {user_input}. "
        f"The provided job data is: {json.dumps(processed_jobs_data)}. "
        f"The provided major data is: {json.dumps(processed_major_data)}. "
        f"The current exam data is: {json.dumps(current_exam_data)}. "
        f"The national exam data is: {json.dumps(national_exam_data)}. "
        f"The qualification categories data is: {json.dumps(qualification_categories_data)}. "
        "Please provide career path and major recommendations that are directly related to the user's interests, job data, major data, exam data, and qualification categories data. "
    )
    
    try:
        response = client.chat.completions.create(
            model='llama3.1',
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": recommendation_prompt}
            ]
        )
        
        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content
        else:
            return "No recommendations generated."
    
    except Exception as e:
        print(f"Error generating career recommendations: {e}")
        return "Error generating recommendations, please try again."
