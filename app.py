from flask import Flask,request,jsonify,render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
     return render_template("index.html")

@app.route("/submit", methods=["POST"])
def get_txt_file():
    # return('HELLO')
    if request.method=='POST':
        f = request.files['textfile']
        f_path = './TextFiles'
        f_name = 'data.txt'
        file_type = f_name.split('.')[1]
        if file_type == 'txt':
            f.save(f'{f_path}/{f_name}')
            with open(f'{f_path}/{f_name}') as l:
                lines = l.readlines()
            return render_template("index.html",success='The text file has been uploaded')
        else:
            return render_template("index.html",failure='Please upload a text file')


@app.route("/scrape", methods=["POST"])
def scrape_data():
    f_path = './TextFiles'
    f_name = 'data.txt'
    temp = open(f'{f_path}/{f_name}','r').read().split('\n')
    return(temp)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
