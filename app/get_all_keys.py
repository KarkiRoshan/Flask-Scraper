import psycopg2
from app import username
from app import password
from app import host
from app import database
from app import port

def get_all_keys():
    with psycopg2.connect(user=username,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT distinct uniquename
                FROM scraped_data;
            """)
            tables = cursor.fetchall()
            table_list = []
            for table in tables:
                table_list.append(table[0])
            return table_list
# print(get_all_keys())