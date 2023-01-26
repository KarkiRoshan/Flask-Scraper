import psycopg2
from app import username
from app import password
from app import host
from app import database
from app import port

def get_data_from_db(keyname):   
    try:
        connection = psycopg2.connect(user=username,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        
        connection.autocommit = True 
        cursor = connection.cursor()
        sql = f"COPY (SELECT index,title,value FROM scraped_data where uniquename='{keyname}') TO STDOUT WITH CSV DELIMITER ','"
        with open("./CSV/downloaded.csv", "w") as file:
            cursor.copy_expert(sql, file)
        status='success'
    except (Exception, psycopg2.Error) as error:
       status=f'{error}'
        # print("Failed to insert record into person table", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
    return status
# print(get_data_from_db('b20230120144947'))