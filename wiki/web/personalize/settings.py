from flask import Flask

app = Flask(__name__.split('.')[0], template_folder='///wiki\\web\\personalize\\templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\School\\NKU\\CSC540\\RikiPersonalizationAPI\\database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
