from app import app 
from flask import request,render_template
from .scrape import scraper
from .formatter import df_formatter
import pandas as pd 
import os 

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
        # links,desc,titles = scraper('apple')
        # # return(render_template[links,desc,titles])
        # return render_template("index.html",data=[len(links),len(desc),len(titles)])
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
    final_df.to_csv(f'{csv_dir}/formatted.csv',index=False)
    return([df.Title[1]])    