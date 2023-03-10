import psycopg2
from app import username
from app import password
from app import host
from app import database
from app import port


def file_info_update(file_path,actual_file_name,now,unique_fname,platform):   
 
    try:
        connection = psycopg2.connect(user=username,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        connection.autocommit = True 
        cursor = connection.cursor()
        create_table = '''CREATE TABLE IF NOT EXISTS scraping_requests(
                                index serial,
                                uniquefilename varchar(50) primary key,
                                time varchar(50),
                                path_to_file varchar(50),
                                original_file_name varchar(50),
                                scraping_status BOOLEAN,
                                platform varchar(10))'''
        cursor.execute(create_table)
        insert_script='''INSERT INTO scraping_requests (uniquefilename,time,path_to_file,original_file_name,scraping_status,platform)
                        VALUES(%s,%s,%s,%s,%s,%s)'''
        insert_values = (unique_fname,now,file_path,actual_file_name,False,platform)      
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

# print(file_info_update('file_path','actual_file_name',"now","unique_fname"))