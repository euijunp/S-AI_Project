import json
from openai import OpenAI
from data_processing import preprocess_and_translate_data  # Corrected function name

client = OpenAI(
    base_url='http://localhost:11434/v1',  # Ollama API 서버 URL
    api_key='ollama',  # 실제로 필요한 경우 올바른 API 키로 설정해야 함
)

def filter_data_by_keyword(data, keyword):
    """
    입력된 데이터에서 사용자가 입력한 키워드와 관련된 정보만 추출합니다.
    """
    filtered_data = []

    for entry in data:
        # 직업 또는 전공 데이터의 각 필드를 확인하고 키워드가 포함된 항목을 필터링
        if any(keyword.lower() in str(value).lower() for value in entry.values()):
            filtered_data.append(entry)

    return filtered_data

def generate_career_recommendations(processed_jobs_data, processed_major_data, user_input):
    print("user input: " + user_input)
    
    # 키워드를 기준으로 관련 데이터 필터링
    keyword = user_input  # 사용자의 입력이 필터링할 키워드로 사용됨
    filtered_jobs_data = filter_data_by_keyword(processed_jobs_data, keyword)
    filtered_major_data = filter_data_by_keyword(processed_major_data, keyword)
    
    # 필터링된 데이터를 JSON 형식으로 변환
    filtered_jobs_json = json.dumps(filtered_jobs_data, ensure_ascii=False, indent=2)
    filtered_majors_json = json.dumps(filtered_major_data, ensure_ascii=False, indent=2)

    # Prepare the recommendation prompt
    recommendation_prompt = (
        f"User's profile: Interests and background: {user_input}. "
        "The user has expressed a strong interest in this particular field, and the career recommendation should be tailored specifically to their passion and interests. "
        "Here is the filtered career data in JSON format based on the user's interest: "
        f"{filtered_jobs_json}. "  # 필터링된 직업 데이터 포함
        "Additionally, here is the filtered major and education data in JSON format: "
        f"{filtered_majors_json}. "  # 필터링된 전공 데이터 포함
        "Please analyze these JSON data sets and use them to provide personalized career recommendations for the user. "
        "Make sure to generate the recommendations based on the fields closely related to the user's interest and provide actionable steps, including educational pathways, certifications, and career prospects."
    )

    # Save input request to input.txt using utf-8 encoding
    try:
        with open("input.txt", "w", encoding="utf-8") as input_file:
            input_file.write(recommendation_prompt)
        
        # API call to generate recommendations
        response = client.chat.completions.create(
            model='llama3.1',
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": recommendation_prompt}
            ]
        )
        
        # Log the request and response for debugging
        print(f"API Request: {recommendation_prompt}")
        print(f"API Response: {response}")
        
        # Save output response to output.txt using utf-8 encoding
        if response.choices and response.choices[0].message.content:
            with open("output.txt", "w", encoding="utf-8") as output_file:
                output_file.write(response.choices[0].message.content)
            return response.choices[0].message.content
        else:
            with open("output.txt", "w", encoding="utf-8") as output_file:
                output_file.write("No recommendations generated.")
            return "No recommendations generated."
    
    except Exception as e:
        error_message = f"Error generating career recommendations: {e}"
        print(error_message)
        
        # Save error message to output.txt using utf-8 encoding
        with open("output.txt", "w", encoding="utf-8") as output_file:
            output_file.write(error_message)
        
        return f"Error generating recommendations: {e}"  # Include exception details in return
