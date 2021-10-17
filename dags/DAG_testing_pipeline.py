import datetime

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python_operator import PythonOperator

from script import main


with DAG(
    dag_id="postgres_operator_dag",
    start_date=datetime.datetime(2021, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    create_sales_table_source = PostgresOperator(
        task_id="create_sales_table_source",
        postgres_conn_id='local_postgres_1',
        sql="""
            CREATE TABLE IF NOT EXISTS sales (
            id SERIAL PRIMARY KEY,
            sales_value INTEGER NOT NULL,
            creation_date DATE NOT NULL);
          """,
    )

    create_sales_table_target = PostgresOperator(
        task_id="create_sales_table_target",
        postgres_conn_id='local_postgres_2',
        sql="""
            CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY,
            sales_value INTEGER NOT NULL,
            creation_date DATE NOT NULL);
          """,
    )

    insert_to_sales_table_source = PythonOperator(
        task_id="insert_to_sales_table_source",
        python_callable=main.generate_random_data,
        op_kwargs={"creation_date": "{{ ds }}"}
    )

    copy_sales_data_source = PythonOperator(
        task_id="copy_sales_data_source",
        python_callable=main.copy_data,
        op_kwargs={"creation_date": "{{ ds }}"}
    )

    check_sales_data_target = PostgresOperator(
        task_id="check_sales_data_target",
        postgres_conn_id='local_postgres_2',
        sql="""
            SELECT *
            FROM sales
            ORDER BY id DESC
            LIMIT 1;
          """,

    )

    create_sales_table_source >> insert_to_sales_table_source >> create_sales_table_target >> copy_sales_data_source >> check_sales_data_target