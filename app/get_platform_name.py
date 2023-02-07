import psycopg2

from app import username
from app import password
from app import host
from app import database
from app import port
def get_platform_name(filename):   
 
    try:
        connection = psycopg2.connect(user=username,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        connection.autocommit = True
        cursor = connection.cursor()
        platformname=f'''SELECT platform 
                         FROM scraping_requests 
                         WHERE uniquefilename='{filename}' '''
        cursor.execute(platformname)  
        rows = cursor.fetchall()  
        # platform_array = []  
        return rows[0][0]

        # status='Data has been successfully uploadedd'
    except (Exception, psycopg2.Error) as error:
       status=f'Data couldnt be uploaded because of {error}'
        # print("Failed to insert record into person table", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()