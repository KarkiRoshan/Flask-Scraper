from app import app 
from flask import request,render_template,send_from_directory
from .scrape import scraper
from .formatter import df_formatter
import pandas as pd 
import os 
from .db_uploader import csv_to_db
from .get_all_tables import get_all_tables
from .files_info_db import file_info_update
from .get_file_path import get_file_path
from .update_db_info import update_df_info
from .get_data_from_db import get_data_from_db

@app.route("/", methods=["GET"])
def index():
     return render_template("index.html")

@app.route("/submit", methods=["POST"])
def get_txt_file():
    if request.method=='POST':
        try:    
            f = request.files['textfile']
            f_path = './TextFiles'
            f_name = f.filename
            file_full_path = f'{f_path}/{f_name}'
            f.save(file_full_path)
            file_info_update(file_full_path)
            return render_template("index.html",success='File uploaded sucessfully')
        except:
            return render_template("index.html",success='File couldnt be uploaded')

@app.route("/scrape", methods=["GET"])
def scrape_data():
    try:
        row = get_file_path()
        full_path = row[0][0]
        scraping_status = row[0][1]
        if not scraping_status:
            search_items = open(full_path,'r').read().split('\n')
            count = 0 
            for search_term in search_items:
                scraper(search_term,count)
                count+=1
            update_df_info(full_path)
            csv_dir = './CSV'
            df = pd.read_csv(f'{csv_dir}/data_file.csv')
            df['Desc'] = df['Desc'].str.replace(".*—","",regex=True)
            df.to_csv(f'{csv_dir}/data_file.csv',index=False)
            final_df =df_formatter(df)
            final_df.to_csv(f'{csv_dir}/data_file.csv',index=False)
            return render_template('index.html',data='DONE')
        else:
            return render_template('index.html',data='The data has already been scraped')
    except:
        return render_template('index.html',data='There is no data file to be scraped')


# @app.route('/format',methods=['GET'])
# def format_data():
#     csv_dir = './CSV'
#     df = pd.read_csv(f'{csv_dir}/data_file.csv')
#     df['Desc'] = df['Desc'].str.replace(".*—","",regex=True)
#     df.to_csv(f'{csv_dir}/data_file.csv',index=False)
#     final_df =df_formatter(df)
#     final_df.to_csv(f'{csv_dir}/data_file.csv',index=False)
#     return('Data Has been formatted')    


@app.route('/uploadtodb',methods=['POST'])
def upload_to_db():
    # return
     if request.method == "POST":
        table_name = request.form['input_text']
        table_list = get_all_tables()
        if table_name in table_list:
            return render_template('index.html',table_name_conflict=f'Please enter another tablename, {table_name} already exists ')
        else:
            status= csv_to_db(table_name)
            return render_template('index.html',table_name_conflict=status)


@app.route('/download',methods=['GET'])
def get_table():
    
        table_list = get_all_tables()
        return render_template('index.html',table_list=table_list)


@app.route('/download/<filename>',methods=['GET'])
def download_table(filename):
        get_data_from_db(filename)
        return send_from_directory('../CSV','downloaded.csv')