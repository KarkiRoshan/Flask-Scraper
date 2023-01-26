import psycopg2
from app import username
from app import password
from app import host
from app import database
from app import port
import csv
def horizontal_data(uniquename):   
 
    try:
        connection = psycopg2.connect(user=username,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        connection.autocommit = True
        cursor = connection.cursor()
        update_query = f'''with searchKey as(
                                select "value" as searchkey,substr("index",1,3) as index_col  from scraped_data  where "title" ='SearchKey' and "uniquename"='{uniquename}'
                            ),
                            title as(
                            select "value" as titles,substr("index",1,3) as index_col  from scraped_data  where "title" ='Title' and "uniquename"='{uniquename}'
                            ),
                            Link as(
                            select "value" as Links,substr("index",1,3) as index_col  from scraped_data  where "title" ='Link' and "uniquename"='{uniquename}'
                            ),
                            Description as(
                            select "value" as Description,substr("index",1,3) as index_col  from scraped_data  where "title" ='Desc' and "uniquename"='{uniquename}'
                            ),
                            final_table as (select searchkey,titles,Links,Description from searchKey inner join title on title.index_col=searchKey.index_col inner join Link 
                            on title.index_col=Link.index_col inner join Description on Description.index_col=Link.index_col)
                            select * from final_table  '''  
        cursor.execute(update_query) 
        rows = cursor.fetchall()  
        with open('./CSV/horizontal.csv', 'w', newline='') as f:
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

