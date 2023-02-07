from app import app 
from flask import request,render_template,send_from_directory,redirect
from .scrape import scraper
from .formatter import df_formatter
import pandas as pd 
from datetime import datetime
import json
import os 
from .db_uploader import csv_to_db
from .get_all_keys import get_all_keys
from .files_info_db import file_info_update
from .get_file_path import get_file_path
from .update_db_info import update_df_info
from .get_data_from_db import get_data_from_db
from .zip import zip
from .horizontal_data import horizontal_data
from .daraz_scrape import daraz_crawler
from .typecast import typecasting
from .get_platform_name import get_platform_name
from .horizontal_daraz import horizontal_daraz
from .api_call import api_data
from .ingredients_formatter import ingredients_formatter
from .horizontal_api import horizontal_api


@app.route("/", methods=["GET"])
def index():
     return render_template("index.html")

@app.route("/submitgoogle", methods=["POST"])
def get_txt_file():
    if request.method=='POST':
        try:    
            f = request.files['textfile']

            actual_f_name = f.filename
            if (actual_f_name.split('.')[-1]=='txt'):
                f_path = './TextFiles'
                now = datetime.now()
                timestamp_filename = now.strftime("%Y-%m-%d-%H-%M-%S")
                unique_fname = actual_f_name.split('.')[0] + ''.join(timestamp_filename.split('-'))

                file_full_path = f'{f_path}/{timestamp_filename}.txt'
                f.save(file_full_path)
                status =file_info_update(file_full_path,actual_f_name,now,unique_fname,'google')
                # return status
                return render_template("index.html",success='File uploaded sucessfully')
            else:
                return render_template("index.html",success='Please Submit a textFile')
        except:
            return render_template("index.html",success='File couldnt be uploaded')
@app.route('/submitdaraz', methods=["POST"])
def get_daraz_txt():
        if request.method=='POST':
                try:    
                        f = request.files['textfile']

                        actual_f_name = f.filename
                        if (actual_f_name.split('.')[-1]=='txt'):
                                f_path = './TextFiles'
                                now = datetime.now()
                                timestamp_filename = now.strftime("%Y-%m-%d-%H-%M-%S")
                                unique_fname = actual_f_name.split('.')[0] + ''.join(timestamp_filename.split('-'))

                                file_full_path = f'{f_path}/{timestamp_filename}.txt'
                                f.save(file_full_path)
                                status =file_info_update(file_full_path,actual_f_name,now,unique_fname,'daraz')
                                # return status
                                return render_template("index.html",success='File uploaded sucessfully')
                        else:
                                return render_template("index.html",success='Please Submit a textFile')
                except:
                        return render_template("index.html",success='File couldnt be uploaded')

@app.route('/submitingredients', methods=["POST"])
def get_ingredients_txt():
        if request.method=='POST':
                try:    
                        f = request.files['textfile']

                        actual_f_name = f.filename
                        if (actual_f_name.split('.')[-1]=='txt'):
                                f_path = './TextFiles'
                                now = datetime.now()
                                timestamp_filename = now.strftime("%Y-%m-%d-%H-%M-%S")
                                unique_fname = actual_f_name.split('.')[0] + ''.join(timestamp_filename.split('-'))

                                file_full_path = f'{f_path}/{timestamp_filename}.txt'
                                f.save(file_full_path)
                                status =file_info_update(file_full_path,actual_f_name,now,unique_fname,'api_data')
                                return render_template("index.html",success_ingredients='File uploaded sucessfully')
                        else:
                                return render_template("index.html",success_ingredients='Please Submit a textFile')
                except:
                        return render_template("index.html",success_ingredients='File couldnt be uploaded')

@app.route("/scrape", methods=["GET"])
def show_unscraped():

        file_array = get_file_path()
        for files in file_array:
            files[0] = files[0].split('/')[-1]
        return render_template('scrape.html',files=file_array)
 

@app.route("/scrape/<filepath>", methods=["GET"])
def scrape_data(filepath):
        csv_dir = './CSV'
        if os.path.exists('./CSV/datafile.csv'):
                os.remove('./CSV/datafile.csv')
        if os.path.exists('./JSON/api_data.json'):
                os.remove('./JSON/api_data.json')
        oldfilename = request.args.get('oldfilename')
        platform = request.args.get('platform')
        oldfilename=oldfilename.split('.')[0]
        time_stamp = filepath.split('-')
        unique_table_name = oldfilename + ''.join(time_stamp)
        search_items = open(f"./TextFiles/{filepath}",'r').read().split('\n')
        count=0
        if platform=='google':
                for search_term in search_items:
                        scraper(search_term,count,unique_table_name.split('.')[0])
                        count+=1
                update_df_info(f"./TextFiles/{filepath}")
                df = pd.read_csv(f'{csv_dir}/data_file.csv')
                df['Desc'] = df['Desc'].str.replace(".*—","",regex=True)
                df.to_csv(f'{csv_dir}/data_file.csv',index=False)
                final_df =df_formatter(df)
                final_df.to_csv(f'{csv_dir}/data_file.csv',index=False)
                return redirect(f'/uploadtodb?arg={unique_table_name}')
        elif platform=='daraz':
                for search_term in search_items:
                        daraz_crawler(search_term,count,unique_table_name.split('.')[0])
                        count+=1
                update_df_info(f"./TextFiles/{filepath}")
                df = pd.read_csv(f'{csv_dir}/data_file.csv')
                df['Price'] = df['Price'].str.replace(",+","",regex=True)
                df['Price'] = df['Price'].str.replace("^Rs.","",regex=True)
                df['Price'] = df['Price'].apply(typecasting)
                df.to_csv(f'{csv_dir}/data_file.csv',index=False)
                final_df = df_formatter(df)
                final_df.to_csv(f'{csv_dir}/data_file.csv',index=False)
                return redirect(f'/uploadtodb?arg={unique_table_name}')
        elif platform=='api_data':
                status = api_data(search_items)
                update_df_info(f"./TextFiles/{filepath}")
                if status=='DONE':
                        with open('./JSON/api_data.json') as f:
                                data = json.loads(f.read())
                        df1 = pd.json_normalize(data,record_path=['missedIngredients'],meta=['title','usedIngredientCount','missedIngredientCount'])
                        df2 = pd.json_normalize(data,record_path=['usedIngredients'],meta=['title','usedIngredientCount','missedIngredientCount'])
                        df1 = df1[['name','unit','amount','title','usedIngredientCount','missedIngredientCount']]
                        df1['type'] = 'missed_ingredient'
                        df2 = df2[['name','unit','amount','title','usedIngredientCount','missedIngredientCount']]
                        df2['type'] = 'used_ingredient'
                        df1 = df1.reset_index()
                        df2 = df2.reset_index()
                        df1 = df1.append(df2)
                        dict = {}
                        for x in data:
                                a=x['title']
                                dict[f'{a}']=x['id']
                        df1['id'] = df1['title'].apply(lambda x : dict[f'{x}'])
                        df1['search_query'] = f'{search_items}'
                        df1.to_csv(f'{csv_dir}/data_file.csv',index=False)
                        final_df = pd.read_csv(f'{csv_dir}/data_file.csv')
                        final_df.drop(['index'],axis=1,inplace=True)
                        df1 = ingredients_formatter(final_df)
                        df1.to_csv(f'{csv_dir}/data_file.csv',index=False)
                        return redirect(f'/uploadtodb?arg={unique_table_name}')
                        
                else:
                        return('Couldnt get the data from api')


@app.route('/uploadtodb',methods=['GET'])
def upload_to_db():
        arg = request.args.get('arg')
        table_name = arg.split('.')[0]
        status= csv_to_db(table_name)
        return render_template('scrape.html',table_name_conflict=status)


@app.route('/download',methods=['GET'])
def get_table(): 
        table_list = get_all_keys()
        return render_template('tables.html',table_list=table_list)


@app.route('/download/<filename>',methods=['GET'])
def download_table(filename):
        # return(filename)
        status = get_data_from_db(filename)
        platform = get_platform_name(filename)
        if platform=='google':
                horizontal_data(filename)
        elif platform=='daraz':
                horizontal_daraz(filename)
        else:
                horizontal_api(filename)
                source_files = ['./CSV/downloaded.csv','./CSV/horizontal.csv']
                zip(source_files,'./ZipFile/zip.zip')
                return send_from_directory('../ZipFile','zip.zip')
        screenshots = os.listdir(f'./Screenshot/{filename}')
        for screenshot in screenshots:
                if screenshot.split('.')[-1] != 'png':
                        inner_dir = os.listdir(f'./Screenshot/{filename}/{screenshot}')
                        for inner_file in inner_dir:
                                source_files.append(f'./Screenshot/{filename}/{screenshot}/{inner_file}')
                else:
                        source_files.append(f'./Screenshot/{filename}/{screenshot}')
        zip(source_files,'./ZipFile/zip.zip')
        return send_from_directory('../ZipFile','zip.zip')