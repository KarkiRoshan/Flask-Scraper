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
        select_last_entry='''select path_to_file,original_file_name,time from scraping_requests where scraping_status=false'''   
        cursor.execute(select_last_entry)  
        rows = cursor.fetchall()  
        file_array = []  
        for file in rows:
            file_array.append([file[0],file[1],file[2]])

        # status='Data has been successfully uploadedd'
    except (Exception, psycopg2.Error) as error:
       status=f'Data couldnt be uploaded because of {error}'
        # print("Failed to insert record into person table", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
    return file_array