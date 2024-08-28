import requests
import json

# API 키와 기본 URL 설정
api_key = 'dce42638afaf57784a701d4b5371cdef'
base_url_jobs = 'https://www.career.go.kr/cnet/front/openapi/jobs.json'
base_url_major = 'https://www.career.go.kr/cnet/openapi/getOpenApi.json'

# 직업백과 데이터 가져오기
def fetch_jobs_data(api_key, page_index=1):
    params = {
        'apiKey': api_key,
        'pageIndex': page_index,
    }
    response = requests.get(base_url_jobs, params=params)
    if response.status_code == 200:
        return response.json().get('jobs', [])
    else:
        print(f"Error fetching jobs data: {response.status_code}")
        return []

# 학과정보 데이터 가져오기
def fetch_major_data(api_key, page=1, per_page=50):
    params = {
        'apiKey': api_key,
        'svcType': 'api',
        'svcCode': 'MAJOR',
        'contentType': 'json',
        'gubun': 'univ_list',
        'thisPage': page,
        'perPage': per_page
    }
    response = requests.get(base_url_major, params=params)
    if response.status_code == 200:
        return response.json().get('dataSearch', {}).get('content', [])
    else:
        print(f"Error fetching major data: {response.status_code}")
        return []

# 데이터 전처리 함수
def preprocess_data(data, data_type='job'):
    processed_data = []
    
    if data_type == 'job':
        for item in data:
            processed_item = {
                'job_name': item.get('job_nm'),
                'work': item.get('work'),
                'aptitude': item.get('aptitudeList', []),
                'related_certificates': item.get('certiList', []),
                'related_departments': item.get('departList', [])
            }
            processed_data.append(processed_item)
    
    elif data_type == 'major':
        for item in data:
            processed_item = {
                'major_name': item.get('title'),
                'major_code': item.get('majorSeq'),
                'university': item.get('univ_name'),
                'department': item.get('department')
            }
            processed_data.append(processed_item)
    
    return processed_data

# 메인 실행 함수
if __name__ == "__main__":
    # 직업백과 데이터 가져오기 및 전처리
    jobs_data = fetch_jobs_data(api_key)
    processed_jobs_data = preprocess_data(jobs_data, data_type='job')
    
    # 학과정보 데이터 가져오기 및 전처리
    major_data = fetch_major_data(api_key)
    processed_major_data = preprocess_data(major_data, data_type='major')
    
    # 결과 출력 또는 파일로 저장
    with open('processed_jobs_data.json', 'w', encoding='utf-8') as f:
        json.dump(processed_jobs_data, f, ensure_ascii=False, indent=4)
    
    with open('processed_major_data.json', 'w', encoding='utf-8') as f:
        json.dump(processed_major_data, f, ensure_ascii=False, indent=4)
    
    print("Data processing completed and saved to JSON files.")