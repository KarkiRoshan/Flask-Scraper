from flask import Flask,render_template
from config import username
from config import password
from config import host
from config import database
from config import port
from config import apiKey

app = Flask(__name__)


from app import views 



