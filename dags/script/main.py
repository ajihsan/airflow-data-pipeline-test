import json
from random import randint

from psycopg2 import connect
from psycopg2.extras import execute_values, RealDictCursor


def connection(username, password, host, port, database):
        conn = connect(
        user=username,
        password=password,
        host=host,
        port=port,
        database=database
        )
        cursor = conn.cursor()
        print("Connect Cursor Postgresql")
        return conn, cursor


def insert_execute(conn, cursor, data:json):
    column = list(data[0].keys())
    final_list_data = []

    for data in data:
        dat = []
        for col in column:
            dat.append(data[col])
        final_list_data.append(tuple(dat))

    insert_query = """
        INSERT INTO sales ({})
        VALUES %s
        ON CONFLICT (id)
        DO NOTHING
        """.format(','.join(column))

    execute_values(
        cursor, insert_query, final_list_data, template=None, page_size=100
    )
    conn.commit()


def generate_random_data(creation_date):
    random_number = randint(1000, 10000)

    data = [{
        "sales_value": random_number,
        "creation_date": creation_date
    }]

    with open ('dags/script/credentials.json', "r") as cred:
        credential_source = json.load(cred)['postgres_source']
    
    conn, cursor = connection(credential_source["username"], credential_source["password"], credential_source["host"], credential_source["port"], credential_source["database"])
    
    insert_execute(conn, cursor, data)
    print('Insert Data to Source {} Success'.format(creation_date))

    cursor.close()
    conn.close()



def copy_data(creation_date):
    with open ('dags/script/credentials.json', "r") as cred:
        credential = json.load(cred)
        credential_source = credential['postgres_source']
        credential_target = credential['postgres_target']

    conn, cursor = connection(credential_source["username"], credential_source["password"], credential_source["host"], credential_source["port"], credential_source["database"])
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    select_query = """
    SELECT * FROM sales
    WHERE creation_date = '{}'
    """.format(creation_date)

    cursor.execute(select_query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    conn, cursor = connection(credential_target["username"], credential_target["password"], credential_target["host"], credential_target["port"], credential_target["database"])

    insert_execute(conn, cursor, data)
    print('Insert Data to Target {} Success'.format(creation_date))

    cursor.close()
    conn.close()