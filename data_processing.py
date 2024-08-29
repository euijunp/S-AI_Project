import requests
import json

# API와 기본 URL 설정
oapi_key = 'dce42638afaf57784a701d4b5371cdef'
base_url_jobs = 'https://www.career.go.kr/cnet/front/openapi/jobs.json'
base_url_major = 'https://www.career.go.kr/cnet/openapi/getOpenApi.json'

# 직업백과 데이터 가져오기 (모든 페이지 처리)
def fetch_all_jobs_data(oapi_key):
    all_jobs = []
    page_index = 1

    while True:
        print(f"\rFetching jobs data for page {page_index}", end="")
        params = {
            'apiKey': oapi_key,
            'pageIndex': page_index,
        }
        try:
            response = requests.get(base_url_jobs, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            jobs = response.json().get('jobs', [])
            if not jobs:
                break  # No more data
            all_jobs.extend(jobs)
            page_index += 1
        except requests.exceptions.RequestException as e:
            print(f"\nError fetching jobs data: {e}")
            break
        except json.JSONDecodeError:
            print("\nError decoding JSON response.")
            break

    print("\nFinished fetching jobs data.")
    return all_jobs

# 학과정보 데이터 가져오기 (모든 페이지 처리)
def fetch_all_major_data(oapi_key, per_page=50):
    all_majors = []
    page = 1

    while True:
        print(f"\rFetching major data for page {page}", end="")
        params = {
            'apiKey': oapi_key,
            'svcType': 'api',
            'svcCode': 'MAJOR',
            'contentType': 'json',
            'gubun': 'univ_list',
            'thisPage': page,
            'perPage': per_page
        }
        try:
            response = requests.get(base_url_major, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            majors = response.json().get('dataSearch', {}).get('content', [])
            if not majors:
                break  # No more data
            all_majors.extend(majors)
            page += 1
        except requests.exceptions.RequestException as e:
            print(f"\nError fetching major data: {e}")
            break
        except json.JSONDecodeError:
            print("\nError decoding JSON response.")
            break

    print("\nFinished fetching major data.")
    return all_majors

# 데이터 전처리 함수
def preprocess_data(data, data_type='job'):
    processed_data = []
    
    if data_type == 'job':
        for item in data:
            processed_item = {
                'job_name': item.get('job_nm'),
                'work': item.get('work'),
                'aptitude': item.get('aptit_name', []),
                'related_certificates': item.get('rel_job_nm', []),
                'related_departments': item.get('wlb', []),
                'wage': item.get('wage'),  # 연봉 수준 정보 추가
                'salary_level': item.get('salaryLevel')  # 연봉 수준의 레벨 정보 추가
            }
            processed_data.append(processed_item)
    
    elif data_type == 'major':
        for item in data:
            processed_item = {
                'major_name': item.get('mClass'),
                'relative_name': item.get('lClass'),
                'major_code': item.get('majorSeq'),
                'department': item.get('facilName')
            }
            processed_data.append(processed_item)
    
    return processed_data

# 데이터 저장 함수
def save_data(jobs_data, major_data):
    try:
        with open('processed_jobs_data.json', 'w', encoding='utf-8') as f:
            json.dump(jobs_data, f, ensure_ascii=False, indent=4)
        print("Jobs data saved to 'processed_jobs_data.json'")
    except (TypeError, IOError) as e:
        print(f"Error saving jobs data to JSON file: {e}")

    try:
        with open('processed_major_data.json', 'w', encoding='utf-8') as f:
            json.dump(major_data, f, ensure_ascii=False, indent=4)
        print("Major data saved to 'processed_major_data.json'")
    except (TypeError, IOError) as e:
        print(f"Error saving major data to JSON file: {e}")

if __name__ == '__main__':
    # 데이터 전처리 및 저장
    jobs_data = fetch_all_jobs_data(oapi_key)
    processed_jobs_data = preprocess_data(jobs_data, data_type='job')

    major_data = fetch_all_major_data(oapi_key)
    processed_major_data = preprocess_data(major_data, data_type='major')

    # 전처리된 데이터 저장
    save_data(processed_jobs_data, processed_major_data)