from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
from pymongo import MongoClient

# MongoDB 연결 설정
def connect_to_mongo():
    client = MongoClient('mongodb://localhost:27017/')  # MongoDB URL
    db = client['my_database']  # 사용할 데이터베이스 이름
    return db['my_collection']  # 사용할 컬렉션 이름

# API에서 데이터 가져오기
def fetch_data_from_api(**kwargs):
    url = "https://api.example.com/data"  # API 엔드포인트
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # 데이터를 반환
    else:
        raise Exception(f"API 요청 실패: {response.status_code}")

# MongoDB에 데이터 저장
def save_to_mongo(**kwargs):
    collection = connect_to_mongo()
    ti = kwargs['ti']  # Task Instance
    data = ti.xcom_pull(task_ids='fetch_data_from_api')  # 이전 태스크에서 데이터 가져오기

    if data:
        collection.insert_many(data)  # 데이터를 MongoDB에 저장
    else:
        raise ValueError("MongoDB에 저장할 데이터가 없습니다.")

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
    schedule_interval=timedelta(days=1),  # DAG 실행 간격
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:
    
    fetch_data = PythonOperator(
        python="/home/kwon/code/.venv/bin/python",
        task_id='fetch_data_from_api',
        python_callable=fetch_data_from_api,
        provide_context=True,
    )

    save_data = PythonOperator(
        python="/home/kwon/code/.venv/bin/python",
        task_id='save_to_mongo',
        python_callable=save_to_mongo,
        provide_context=True,
    )

    fetch_data >> save_data
