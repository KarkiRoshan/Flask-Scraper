import psycopg2
from app import username
from app import password
from app import host
from app import database
from app import port

import csv
def horizontal_daraz(uniquename):   
 
    try:
        connection = psycopg2.connect(user=username,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        connection.autocommit = True
        cursor = connection.cursor()
        update_query = f'''WITH 
                            searchKey AS(
                                SELECT "value" AS searchkey,substr("index",1,3) AS index_col  
                                FROM scraped_data  
                                WHERE "title" ='SearchKey' and "uniquename"='{uniquename}'
                            ),
                            title AS(
                                SELECT "value" AS titles,substr("index",1,3) AS index_col  
                                FROM scraped_data  
                                WHERE "title" ='Title' and "uniquename"='{uniquename}'
                            ),
                            price AS(
                                SELECT "value" AS price,substr("index",1,3) AS index_col  
                                FROM scraped_data  
                                WHERE "title" ='Price' and "uniquename"='{uniquename}'
                            ),
                            SELECT 
                            searchkey,titles,price 
                            FROM searchKey 
                            INNER JOIN title ON title.index_col=searchKey.index_col 
                            INNER JOIN price ON title.index_col=price.index_col)
                        '''  
        cursor.execute(update_query) 
        rows = cursor.fetchall()  
        with open('./CSV/horizontal.csv', 'w', newline='',encoding='UTF-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
    except (Exception, psycopg2.Error) as error:
       print(f'Data couldnt be uploaded because of {error}')
        # print("Failed to insert record into person table", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
