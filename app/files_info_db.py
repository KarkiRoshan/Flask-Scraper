import psycopg2
from app import username
from app import password
from app import host
from app import database
from app import port

def file_info_update(file_path):   
 
    try:
        connection = psycopg2.connect(user=username,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        connection.autocommit = True 
        cursor = connection.cursor()
        create_table = '''CREATE TABLE IF NOT EXISTS scraping_requests(
                                index serial primary key,
                                time timestamp default now(),
                                path_to_file varchar(50),
                                scraping_status BOOLEAN)'''
        cursor.execute(create_table)
        insert_script='''INSERT INTO scraping_requests (path_to_file,scraping_status)
                        VALUES(%s,%s)'''
        insert_values = (file_path,False)      
        cursor.execute(insert_script,insert_values)     
        status='Data has been successfully uploadedd'
    except (Exception, psycopg2.Error) as error:
       status=f'Data couldnt be uploaded because of {error}'
        # print("Failed to insert record into person table", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
    return status