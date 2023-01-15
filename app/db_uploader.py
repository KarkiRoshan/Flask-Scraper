import psycopg2
from app import username
from app import password
from app import host
from app import database
from app import port


def csv_to_db(table_name):   
 
    try:
        connection = psycopg2.connect(user=username,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        connection.autocommit = True 
        cursor = connection.cursor()
        create_table = f'''CREATE TABLE IF NOT EXISTS {table_name}(
                                index varchar(10) Primary Key,
                                title varchar(100),
                                value varchar(200))'''
        cursor.execute(create_table)
        copy_csv = f'''COPY {table_name}(Title,value,index)
                        FROM 'D:\\Users\\Predator\\Internship\\FlaskApp1\\CSV\\data_file.csv'
                        DELIMITER ','
                        CSV HEADER;'''
        cursor.execute(copy_csv)
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
