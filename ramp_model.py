import json
from openai import OpenAI
from data_processing import fetch_all_jobs_data, fetch_all_major_data, preprocess_data

# OpenAI 클라이언트 설정
client = OpenAI(
    base_url='http://localhost:11434/v1',  # Ollama API 서버 URL
    api_key='ramp',  # Ollama API 키 (실질적으로 사용 안 함.)
)

def generate_career_recommendations(jobs_data, major_data, user_input):
    # Example logic for generating recommendations
    # Ensure this returns a list of recommendations
    recommendations = []

    # Logic to populate recommendations based on user input
    # For example, matching user_input with job descriptions or majors
    for job in jobs_data:
        if user_input.lower() in job['job_name'].lower() or user_input.lower() in job['work'].lower():
            recommendations.append(job['job_name'])
    
    for major in major_data:
        if user_input.lower() in major['major_name'].lower():
            recommendations.append(major['major_name'])
    
<<<<<<< HEAD
    except Exception as e:
        print(f"Error generating career recommendations: {e}")
        return None
    
    except Exception as e:
        print(f"Error generating career recommendations: {e}")
        return None
=======
    return recommendations  # This must be a list
>>>>>>> f16b683e81832f9dd0ee4490ec3f2514b5882d08
