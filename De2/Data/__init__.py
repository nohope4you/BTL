from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import  LoginManager
from flask_babelex import Babel
import cloudinary


app = Flask(__name__)
app.secret_key='wd21421def23r23rfe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/hotel?charset=utf8mb4' % quote('Meo123123123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CART_KEY']='cart'

cloudinary.config(cloud_name='den9v9scv', api_key='946921511849563', api_secret='JZUnG5keb290a-ysdlOkVBnfH6w')



db= SQLAlchemy(app=app)


login = LoginManager(app = app)

babel = Babel(app=app)


@babel.localeselector
def load_locate():
    return 'vi'