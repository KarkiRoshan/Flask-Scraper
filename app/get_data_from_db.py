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
        query = f'''COPY (SELECT index,title,value 
                          FROM scraped_data 
                          WHERE uniquename='{keyname}') TO STDOUT WITH CSV DELIMITER ',' '''
        with open("./CSV/vertical.csv", "w",encoding='utf-8') as file:
            cursor.copy_expert(query, file)
        return('success')
    except (Exception, psycopg2.Error) as error:
       status=f'{error}'
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
    return status
