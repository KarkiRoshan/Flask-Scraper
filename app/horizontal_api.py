import psycopg2
from app import username
from app import password
from app import host
from app import database
from app import port


import csv
def horizontal_api(uniquename):   
    try:
        connection = psycopg2.connect(user=username,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        connection.autocommit = True
        cursor = connection.cursor()
        update_query = f'''WITH 
                            searchKey as(
                                SELECT "value" as searchkey,regexp_replace(index, '\.[0-9]+$', '')  as index_col  
                                FROM scraped_data  
                                WHERE "title" ='search_query' and "uniquename"='{uniquename}'
                            ),
                            ingredient_name as(
                                SELECT "value" as ingredient_name,regexp_replace(index, '\.[0-9]+$', '') AS index_col  
                                FROM scraped_data  
                                WHERE "title" ='name' and "uniquename"='{uniquename}'
                            ),
                            unit as(
                                SELECT "value" as unit,regexp_replace(index, '\.[0-9]+$', '') AS index_col  
                                FROM scraped_data  
                                WHERE "title" ='unit' and "uniquename"='{uniquename}'
                            ),
                            amount as(
                                SELECT "value" as amount,regexp_replace(index, '\.[0-9]+$', '') AS index_col  
                                FROM scraped_data  
                                WHERE "title" ='amount' and "uniquename"='{uniquename}'
                            ),
                            title as(
                                SELECT "value" as title,regexp_replace(index, '\.[0-9]+$', '') AS index_col  
                                FROM scraped_data  
                                WHERE "title" ='title' and "uniquename"='{uniquename}'
                            ),
                            usedIngredientCount as(
                                SELECT "value" as usedIngredientCount,regexp_replace(index, '\.[0-9]+$', '') AS index_col  
                                FROM scraped_data  
                                WHERE "title" ='usedIngredientCount' and "uniquename"='{uniquename}'
                            ),
                            missedIngredientCount as(
                                SELECT "value" as missedIngredientCount,regexp_replace(index, '\.[0-9]+$', '') AS index_col  
                                FROM scraped_data  
                                WHERE "title" ='missedIngredientCount' and "uniquename"='{uniquename}'
                            ),
                            ingredient_type as(
                                SELECT "value" as ingredient_type,regexp_replace(index, '\.[0-9]+$', '') AS index_col  
                                FROM scraped_data  
                                WHERE "title" ='type' and "uniquename"='{uniquename}'
                            ),
                            id as(
                                SELECT "value" as id,regexp_replace(index, '\.[0-9]+$', '') AS index_col  
                                FROM scraped_data  
                                WHERE "title" ='id' and "uniquename"='{uniquename}'
                            )
                            SELECT id,ingredient_type,missedIngredientCount,usedIngredientCount,title,unit,ingredient_name,searchKey 
                            FROM id 
                            INNER JOIN ingredient_type ON ingredient_type.index_col=id.index_col 
                            INNER JOIN missedIngredientCount ON missedIngredientCount.index_col=ingredient_type.index_col 
                            INNER JOIN usedIngredientCount ON usedIngredientCount.index_col=missedIngredientCount.index_col
                            INNER JOIN title ON title.index_col=missedIngredientCount.index_col
                            INNER JOIN amount ON amount.index_col=title.index_col 
                            INNER JOIN unit ON amount.index_col=unit.index_col 
                            INNER JOIN ingredient_name ON amount.index_col=ingredient_name.index_col 
                            INNER JOIN searchKey ON searchKey.index_col=ingredient_name.index_col 
						'''  
        cursor.execute(update_query) 
        rows = cursor.fetchall()  
        with open('./CSV/horizontal.csv', 'w', newline='',encoding='UTF-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        # end = perf_counter()
        # print(end-start)
    except (Exception, psycopg2.Error) as error:
       print(f'Data couldnt be uploaded because of {error}')
        # print("Failed to insert record into person table", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
    
