import psycopg2
from app import username
from app import password
from app import host
from app import database
from app import port

def get_file_path():   
 
    try:
        connection = psycopg2.connect(user=username,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        connection.autocommit = True
        cursor = connection.cursor()
        select_last_entry='''select path_to_file,scraping_status from scraping_requests where index in (select max(index) from scraping_requests)'''   
        cursor.execute(select_last_entry)  
        rows = cursor.fetchall()   

        status='Data has been successfully uploadedd'
    except (Exception, psycopg2.Error) as error:
       status=f'Data couldnt be uploaded because of {error}'
        # print("Failed to insert record into person table", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
    return rows
