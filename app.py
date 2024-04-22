from datetime import datetime
from flask import Flask,redirect,url_for,render_template,request, jsonify
from pymongo import MongoClient
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGO_URL = os.environ.get('MONGODB_URL')
DB_NAME = os.environ.get('DB_NAME')

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

app=Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    data = db.fruits.find({})
    return render_template('dashboard.html', fruits=data)

@app.route('/fruits', methods=['GET', 'POST'])
def fruit():
    data = db.fruits.find({})
    return render_template('index.html', fruits=data)

@app.route('/add', methods=['GET', 'POST'])
def addFruit():
    if request.method == 'POST':
        name = request.form['fruitName']
        price = request.form['price']
        description = request.form['description']
        img = request.files['image']
        current_date = datetime.now().strftime('%m%Y%H%M%S')
        
        if img:
            extension = img.filename
            img_path = f'static/assets/img/fruits/{current_date}-{extension}'
            img.save(img_path)
        else:
            img_name = None
        data = {
            'name' : name,
            'price': price,
            'description': description,
            'img': img_path
        }
        db.fruits.insert_one(data)
        return redirect(url_for('fruit'))

    return render_template('AddFruit.html')

@app.route('/edit', methods=['GET', 'POST'])
def editFruit():
    return render_template('EditFruit.html')

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)