# import pkg
from enum import unique
import os
from datetime import date
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
# from flask_migrate import Migrate


# Get absolute path position
# basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

class Config(object):
    user = 'root'
    password = '123'
    # change to name of your database; add path if necessary
    database = 'trip-ticketsDB'
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{}:{}@localhost:3306/{}'.format(user, password, database)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SECRET_KEY'] = 'hardsecretkey'

    # Configure sqlalchemy to automatically update the tracking database
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # When querying, the original SQL statement will be displayed
    app.config['SQLALCHEMY_ECHO'] = False
    # Prohibition of automatic submission of data for processing
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False

app.config.from_object(Config)
# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)
db.init_app(app)

class CrawlerData(db.Model):

    __tablename__ = 'Test_Table'
    # id = db.Column('ID', db.Integer, primary_key=True, autoincrement=True)
    # date = db.Column('Date', db.String(255), unique=False, nullable=False)
    # name = db.Column('Name', db.String(255), unique=False, nullable=False)
    # time = db.Column('Time', db.String(255), unique=False, nullable=False)

    num = db.Column('Num', db.Integer, primary_key=True, autoincrement=True)
    id = db.Column('Id', db.Integer, unique=False, nullable=False)
    location = db.Column('Location', db.String(255), unique=False, nullable=False)
    title = db.Column('Title', db.String(255), unique=False, nullable=False)
    rate = db.Column('Rate', db.String(255), unique=False, nullable=False)
    market_price = db.Column('Market_price', db.Integer, unique=False, nullable=False)
    sell_price = db.Column('Sell_price', db.Integer, unique=False, nullable=False)
    link = db.Column('Link', db.String(255), unique=False, nullable=False)
    timestamp = db.Column('Timestamp', db.Integer, unique=False, nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, num, id, location, title, rate, market_price, sell_price, link, timestamp):
        self.num = num
        self.id = id
        self.location = location
        self.title = title
        self.rate = rate
        self.market_price = market_price
        self.sell_price = sell_price
        self.link = link
        self.link = timestamp

    def __repr__(self):
        return f'Num: {self.num} Id: {self.id} Location: {self.location} Title: {self.title} Rate: {self.rate} Market_price: {self.market_price} Sell_price: {self.sell_price} Link: {self.link} imestamp: {self.timestamp}'

# Models
@app.route('/home')
def home():
    return render_template('index.html', datas= CrawlerData.query.all(), count = CrawlerData.query.count())

@app.route('/about')
def about():
    return render_template('about.html', title='Show Datas')



# Set URL routing and accepted method(default is GET)
# @app.route("/", methods = ['POST', 'GET'])
# def index():
#     # CrawlerData.query.count()
#     return render_template("layout.html", datas=CrawlerData.query.all(), title='Show Datas')


@app.route('/testDB')
def testDB():
    try:
        datas = CrawlerData.query.filter_by(id='1').order_by(CrawlerData.name).all()

        data_text = '<ul>'
        for data in datas:
            data_text += '<li>' + data.name + ', ' + data.date + '</li>'
        data_text += '</ul>'
        return data_text
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


"""
mysql> describe Test_Table1;
+-------+------------------+------+-----+---------+----------------+
| Field | Type             | Null | Key | Default | Extra          |
+-------+------------------+------+-----+---------+----------------+
| Id    | int(11) unsigned | NO   | PRI | NULL    | auto_increment |
| Date  | varchar(255)     | YES  |     | NULL    |                |
| Name  | varchar(255)     | YES  |     | NULL    |                |
| Time  | varchar(255)     | YES  |     | NULL    |                |
+-------+------------------+------+-----+---------+----------------+
4 rows in set (0.00 sec)

mysql> select * from Test_Table1;
+----+------------+------+-------+
| Id | Date       | Name | Time  |
+----+------------+------+-------+
|  1 | 2022/01/18 | 2330 | 14:30 |
|  2 | 2022/01/18 | 2454 | 14:30 |
|  3 | 2022/01/18 | 3231 | 14:30 |
|  4 | 2022/01/18 | 2382 | 14:30 |
|  5 | 2022/01/18 | 4938 | 14:30 |
|  6 | 2022/01/18 | 2317 | 14:30 |
+----+------------+------+-------+
6 rows in set (0.00 sec)

mysql> select * from Test_Table;
+--------------+------------------+------+-----+---------+----------------+
| Field        | Type             | Null | Key | Default | Extra          |
+--------------+------------------+------+-----+---------+----------------+
| Num          | int(11) unsigned | NO   | PRI | NULL    | auto_increment |
| Id           | int(11) unsigned | NO   |     | NULL    |                |
| Location     | varchar(255)     | YES  |     | NULL    |                |
| Title        | varchar(255)     | YES  |     | NULL    |                |
| Rate         | varchar(255)     | YES  |     | NULL    |                |
| Market_price | int(11)          | YES  |     | NULL    |                |
| Sell_price   | int(11)          | YES  |     | NULL    |                |
| Link         | varchar(255)     | YES  |     | NULL    |                |
| Timestamp    | int(11)          | YES  |     | NULL    |                |
+--------------+------------------+------+-----+---------+----------------+
9 rows in set (0.01 sec)
"""



if __name__ == '__main__':
    # user1 = CrawlerData(date='2022/01/20',name='wang',time='14:30')
    # user2 = CrawlerData(date='2022/01/21',name='zhang',time='14:30')
    # user3 = CrawlerData(date='2022/01/22',name='chen',time='14:30')
    # user4 = CrawlerData(date='2022/01/23',name='zhou',time='14:30')
    # db.session.add_all([user1,user2,user3,user4])
    # db.session.commit()

    # db.drop_all()
    # db.create_all()
    app.run(host='localhost', port=8080, debug=True, threaded=True)

