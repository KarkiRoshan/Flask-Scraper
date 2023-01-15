from app import app 
from flask import request,render_template
from .scrape import scraper
from .formatter import df_formatter
import pandas as pd 
import os 
from .db_uploader import csv_to_db
from .get_all_tables import get_all_tables


@app.route("/", methods=["GET"])
def index():
     return render_template("index.html")

@app.route("/submit", methods=["POST"])
def get_txt_file():
    if request.method=='POST':
        f = request.files['textfile']
        f_path = './TextFiles'
        f_name = 'data.txt'
        f.save(f'{f_path}/{f_name}')
        return render_template("index.html",success='asd')
        # else:
        #     return render_template("index.html",failure='Please upload a text file')


@app.route("/scrape", methods=["GET"])
def scrape_data():
    try:
        f_path = './TextFiles'
        f_name = 'data.txt'
        search_items = open(f'{f_path}/{f_name}','r').read().split('\n')
        count = 0 
        for search_term in search_items:
            scraper(search_term,count)
            count+=1
        os.remove(f'{f_path}/data.txt')
        return render_template('index.html',data='DONE')
    except:
        return render_template('index.html',data='There is no data file to be scraped')


@app.route('/format',methods=['GET'])
def format_data():
    csv_dir = './CSV'
    df = pd.read_csv(f'{csv_dir}/data_file.csv')
    df['Desc'] = df['Desc'].str.replace(".*—","",regex=True)
    df.to_csv(f'{csv_dir}/data_file.csv',index=False)
    final_df =df_formatter(df)
    final_df.to_csv(f'{csv_dir}/data_file.csv',index=False)
    return('Data Has been formatted')    


@app.route('/uploadtodb',methods=['POST'])
def upload_to_db():
    
     if request.method == "POST":
        table_name = request.form['user_input']
        table_list = get_all_tables()
        if table_name in table_list:
            return(f'Please enter another tablename, {table_name} already exists ')
        else:
            status= csv_to_db(table_name)
            return([status])


@app.route('/downloaddata',methods=['GET'])
def get_data():
    
     if request.method == "POST":
        table_name = request.form['user_input']
        table_list = get_all_tables()
        if table_name in table_list:
            return(f'Please enter another tablename, {table_name} already exists ')
        else:
            status= csv_to_db(table_name)
            return([status])



