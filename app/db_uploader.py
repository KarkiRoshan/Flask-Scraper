import psycopg2
from app import username
from app import password
from app import host
from app import database
from app import port

import pandas as pd 
def csv_to_db(uniquename):   
 
    try:
        connection = psycopg2.connect(user=username,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        connection.autocommit = True 
        cursor = connection.cursor()
        create_table = f'''CREATE TABLE IF NOT EXISTS scraped_data(
                                id serial primary key,
                                index varchar(10),
                                title varchar(100),
                                value varchar(300),
                                uniquename varchar(50),
                                foreign key (uniquename) references scraping_requests("uniquefilename"))'''
        cursor.execute(create_table)
        df = pd.read_csv('./CSV/data_file.csv')
        for row in df.itertuples():
            insert_script='''INSERT INTO scraped_data (index,title, value,uniquename)
                            VALUES(%s,%s,%s,%s)'''
            insert_values = (row.index,row.Title,row.Value,uniquename)      
            cursor.execute(insert_script,insert_values) 
        status='Uploaded'
    except (Exception, psycopg2.Error) as error:
       status=f'{error}'
        # print("Failed to insert record into person table", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
    return status
# print(csv_to_db('b20230120115312'))