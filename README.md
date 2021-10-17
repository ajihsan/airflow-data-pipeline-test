# Airflow Data Pipeline Test
This repository contains Docker-Compose of Apache Airflow and PostgeSQL. This is the setup for the data pipeline of a basic data warehouse using Docker and Apache Airflow.

![source](https://github.com/ajihsan/airflow-data-pipeline-test/blob/df936715d03978623a23d581b6eaa7087558d245/list_dag.png?raw=true)

There are 5 Operator in this DAG:
1. Create Table in Source Database
2. Insert Table in Source Database with random data
3. Create Table in Target Database
4. Copy Table from Source Database to Target Database
5. Check Table in Target Database

![source](https://github.com/ajihsan/airflow-data-pipeline-test/blob/df936715d03978623a23d581b6eaa7087558d245/dag.png?raw=true) 

## Informations
- Based on Airflow (2.2.0) official Image [apache/airflow:2.2.0](https://hub.docker.com/r/apache/airflow) and uses the official Postgres as backend and Redis as queue
- Based on PostgreSQL (13) official Image [postgres:13](https://hub.docker.com/_/postgres)
- Airflow Webserver are exposed in localhost port 5884
- Postgres for Source Database are exposed in localhost port 5432
- Postgres for Target Database are exposed in localhost port 5433


## Prerequisites
- Install Docker
- Install Docker Compose


## Installation
1. Clone this repository.

```bash
git clone https://github.com/ajihsan/airflow-data-pipeline-test.git
```

2. Run Docker-Compose.
```bash
docker-compose up -d
```

## Usage
1. Setup Connection for Postgres Source Database and Postgres Target Database (based on credential in **database.env**) in Airflow Webserver Panel **Admin->Connections**

![source](https://github.com/ajihsan/airflow-data-pipeline-test/blob/df936715d03978623a23d581b6eaa7087558d245/postgres_source_setting.png?raw=true) 
![target](https://github.com/ajihsan/airflow-data-pipeline-test/blob/df936715d03978623a23d581b6eaa7087558d245/postgres_target_setting.png?raw=true)

2. Unpause DAG from Airflow Webserver
3. Trigger DAG
4. Check the log of each Operators in DAG

## Contact
Muhammad Ihsan - [ajihsan96@gmail.com](mailto:ajihsan96@gmail.com)

Project Link: [https://github.com/ajihsan](https://github.com/ajihsan)
