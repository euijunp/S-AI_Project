import requests
import json
from deep_translator import GoogleTranslator

# API와 기본 URL 설정
oapi_key = 'dce42638afaf57784a701d4b5371cdef'
base_url_jobs = 'https://www.career.go.kr/cnet/front/openapi/jobs.json'
base_url_major = 'https://www.career.go.kr/cnet/openapi/getOpenApi.json'

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
            print(f"\nNumber of jobs fetched: {len(jobs)}")
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

def translate_text(text, target_language='en'):
    if not text:
        return text
    try:
        translator = GoogleTranslator(target_lang=target_language)
        translated_text = translator.translate(text)
        return translated_text
    except Exception as e:
        print(f"Error translating text: {e}")
        return text

def preprocess_and_translate_data(data, data_type='job'):
    processed_data = []
    
    if data_type == 'job':
        for index, item in enumerate(data):
            print(f"Processing job data item {index + 1} / {len(data)}")
            processed_item = {
                'job_name': translate_text(item.get('job_nm', '')),
                'work': translate_text(item.get('work', '')),
                'aptitude': translate_text(item.get('aptit_name', '')),
                'related_certificates': translate_text(item.get('rel_job_nm', '')),
                'related_departments': translate_text(item.get('wlb', '')),
                'wage': translate_text(item.get('wage', '')),
                'salary_level': translate_text(item.get('salaryLevel', ''))
            }
            processed_data.append(processed_item)
    
    elif data_type == 'major':
        for index, item in enumerate(data):
            print(f"Processing major data item {index + 1} / {len(data)}")
            processed_item = {
                'major_name': translate_text(item.get('mClass', '')),
                'relative_name': translate_text(item.get('lClass', '')),
                'major_code': item.get('majorSeq'),
                'department': translate_text(item.get('facilName', ''))
            }
            processed_data.append(processed_item)
    
    return processed_data

def save_data(jobs_data, major_data):
    try:
        if jobs_data is not None:
            with open('processed_jobs_data.json', 'w', encoding='utf-8') as f:
                json.dump(jobs_data, f, ensure_ascii=False, indent=4)
            print(f"Jobs data saved to 'processed_jobs_data.json' with {len(jobs_data)} entries.")
        if major_data is not None:
            with open('processed_major_data.json', 'w', encoding='utf-8') as f:
                json.dump(major_data, f, ensure_ascii=False, indent=4)
            print(f"Major data saved to 'processed_major_data.json' with {len(major_data)} entries.")
    except (TypeError, IOError) as e:
        print(f"Error saving data to JSON file: {e}")

if __name__ == '__main__':
    jobs_data = fetch_all_jobs_data(oapi_key)
    processed_jobs_data = preprocess_and_translate_data(jobs_data, data_type='job')

    major_data = fetch_all_major_data(oapi_key)
    processed_major_data = preprocess_and_translate_data(major_data, data_type='major')

    save_data(processed_jobs_data, processed_major_data)