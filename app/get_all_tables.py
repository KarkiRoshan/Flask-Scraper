import psycopg2
from app import username
from app import password
from app import host
from app import database
from app import port

def get_all_tables():
    with psycopg2.connect(user=username,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            table_list = []
            for table in tables:
                table_list.append(table[0])
            return table_list
get_all_tables()