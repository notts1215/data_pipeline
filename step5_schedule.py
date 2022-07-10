# -- coding: utf-8 --
"""
@Time : 2022/7/10 23:05
@Author : Notts XIANG
@Description : A sample Airflow scheduler
"""

from datetime import timedelta
from datetime import datetime as dt
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
import pendulum

local_tz = pendulum.timezone("Asia/Shanghai")
default_args = {
    'owner': 'notts',
    'depends_on_past': True,
    'start_date': dt(2022, 7, 10, tzinfo=local_tz),
    'email': ['xxxxx@xx.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(hours=1)
}

yesterday_date = "{{ ds_nodash }}"

DAG_ID = "sample pipeline for image processing"
with DAG(DAG_ID, default_args=default_args, schedule_interval="10 1 * * *") as dag:
    step1_extraction = BashOperator(
        task_id="step1_extraction",
        bash_command=f"python /.....PATH CONFIGURED.../step1_extraction.py",
        dag=dag
    )

    step2_transformation = BashOperator(
        task_id="step2_transformation",
        bash_command=f"python /.....PATH CONFIGURED.../step2_transformation.py",
        dag=dag
    )

    step3_load_ods = BashOperator(
        task_id="step3_load_ods",
        bash_command=f'spark-submit --num-executors 1 --executor-cores 2 --executor-memory 1G --driver-memory 1G /.....PATH CONFIGURED.../step3_load_ods.py -i1 {yesterday_date}',
        dag=dag
    )

    step3_load_dwd = BashOperator(
        task_id="step3_load_dwd",
        bash_command=f'spark-submit --num-executors 1 --executor-cores 2 --executor-memory 1G --driver-memory 1G /.....PATH CONFIGURED.../step3_load_dwd.py -i1 {yesterday_date}',
        dag=dag
    )

    step1_extraction >> step2_transformation >> step3_load_ods >> step3_load_dwd

    # If step3_load_ods has another task followed, the DAG can be:
    # step1_extraction >> step2_transformation >> step3_load_ods >> [xxx, step3_load_dwd]
