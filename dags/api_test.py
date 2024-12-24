from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
from pymongo import MongoClient

# MongoDB 연결 설정
def connect_to_mongo():
    try:
        client = MongoClient('mongodb://root:example@192.168.105.199:27017/')  # MongoDB URL
        db = client['my_database']  # 사용할 데이터베이스 이름
        return db['my_collection']  # 사용할 컬렉션 이름
    except Exception as e:
        raise Exception(f"MongoDB 연결 실패: {e}")

# GET API에서 데이터 가져오기
def fetch_data_from_api(**kwargs):
    try:
        url = "http://192.168.105.199:3000/api/data"  # API 엔드포인트
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("GET 요청 데이터:", data)

            # 데이터 타입 검증 및 변환
            if isinstance(data, dict):
                data = [data]  # 단일 객체를 리스트로 변환
            elif not isinstance(data, list):
                raise ValueError("GET 요청의 응답 데이터가 리스트나 객체 형식이 아닙니다.")

            return data
        else:
            raise Exception(f"GET API 요청 실패: {response.status_code}")
    except Exception as e:
        raise Exception(f"GET API 데이터 가져오기 중 오류 발생: {e}")

# POST API에서 데이터 가져오기
def fetch_data_from_api_post(**kwargs):
    try:
        url = "http://192.168.105.199:3000/api/data"  # API 엔드포인트
        response = requests.post(url)

        if response.status_code in [200, 201]:
            data = response.json()
            print("POST 요청 데이터:", data)

            # 데이터 타입 검증 및 변환
            if isinstance(data, dict):
                data = [data]  # 단일 객체를 리스트로 변환
            elif not isinstance(data, list):
                raise ValueError("POST 요청의 응답 데이터가 리스트나 객체 형식이 아닙니다.")

            return data
        else:
            raise Exception(f"POST API 요청 실패: {response.status_code}")
    except Exception as e:
        raise Exception(f"POST API 데이터 가져오기 중 오류 발생: {e}")

# MongoDB에 데이터 저장
def save_to_mongo(task_id, **kwargs):
    try:
        collection = connect_to_mongo()
        ti = kwargs['ti']  # Task Instance
        data = ti.xcom_pull(task_ids=task_id)  # 특정 태스크에서 데이터 가져오기
        print(f"MongoDB에 저장할 데이터 ({task_id}):", data)

        # 데이터 검증 및 저장
        if not data:
            raise ValueError(f"MongoDB에 저장할 데이터가 없습니다. (태스크: {task_id})")

        if isinstance(data, list):
            collection.insert_many(data)  # 리스트 데이터 저장
            print(f"데이터 저장 완료 (리스트, 태스크: {task_id}):", data)
        else:
            raise ValueError(f"MongoDB에 저장할 데이터 형식이 올바르지 않습니다. (태스크: {task_id})")
    except Exception as e:
        raise Exception(f"MongoDB에 데이터 저장 중 오류 발생 (태스크: {task_id}): {e}")

# DAG 정의
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'api_to_mongo',
    default_args=default_args,
    description='API에서 데이터를 가져와 MongoDB에 저장하는 DAG',
    schedule_interval=timedelta(minutes=1),  # DAG 실행 간격
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:
    # GET 요청 태스크
    fetch_data = PythonOperator(
        task_id='fetch_data_from_api',
        python_callable=fetch_data_from_api,
        provide_context=True,
    )

    save_get = PythonOperator(
        task_id='save_get_to_mongo',
        python_callable=save_to_mongo,
        op_kwargs={'task_id': 'fetch_data_from_api'},  # 특정 태스크 ID 전달
        provide_context=True,
    )

    # POST 요청 태스크
    fetch_data_post = PythonOperator(
        task_id='fetch_data_from_api_post',
        python_callable=fetch_data_from_api_post,
        provide_context=True,
    )

    save_post = PythonOperator(
        task_id='save_post_to_mongo',
        python_callable=save_to_mongo,
        op_kwargs={'task_id': 'fetch_data_from_api_post'},  # 특정 태스크 ID 전달
        provide_context=True,
    )

    # 작업 흐름 정의
    fetch_data >> save_get
    fetch_data_post >> save_post
