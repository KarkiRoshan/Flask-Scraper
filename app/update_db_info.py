import psycopg2
# from app import username
# from app import password
# from app import host
# from app import database
# from app import port

username = 'postgres'
password = '599433'
host = 'localhost'
database = 'scraper'
port = '5432'
def update_df_info(path):   
 
    try:
        connection = psycopg2.connect(user=username,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        connection.autocommit = True
        cursor = connection.cursor()
        update_query = f"UPDATE scraping_requests SET scraping_status = True  WHERE path_to_file = '{path}'"   
        cursor.execute(update_query)   

        print('Data has been successfully uploadedd')
    except (Exception, psycopg2.Error) as error:
       print(f'Data couldnt be uploaded because of {error}')
        # print("Failed to insert record into person table", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()

update_df_info('./TextFiles/Google.txt')
