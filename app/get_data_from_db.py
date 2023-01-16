import psycopg2
from app import username
from app import password
from app import host
from app import database
from app import port

# username = 'postgres'
# password = '599433'
# host = 'localhost'
# database = 'scraper'
# port = '5432'

def get_data_from_db(table_name):   
 
    try:
        connection = psycopg2.connect(user=username,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        connection.autocommit = True 
        cursor = connection.cursor()
        sql = f"COPY (SELECT * FROM {table_name} ) TO STDOUT WITH CSV DELIMITER ','"
        with open("../CSV/downloaded.csv", "w") as file:
            cursor.copy_expert(sql, file)
        status='success'
    except (Exception, psycopg2.Error) as error:
       status='failed'
        # print("Failed to insert record into person table", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
    return status
