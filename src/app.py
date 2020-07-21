import os
from flask import (Flask, render_template, request, redirect, url_for, flash)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

# PostegreSQL connection for Docker
db_url = 'localhost:5432'
db_name = 'crud'
db_user = 'postgres'
db_password = '!QWEqwe123'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # PostegreSQL connection for Heroku
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
#     'sqlite:///db.sqlite'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # SQLite3 local connection
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name,email,phone):
        self.name = name
        self.email = email
        self.phone = phone

@app.route('/')
def index():
    def str_to_color(string):
        hash = 0
        for x in string:
            hash = ord(x) + ((hash << 5) - hash)
        c = (hash & 0x00FFFFFF)

        return "00000{}".format(str(c))[-6:]

    all_data = Data.query.order_by(Data.name).all()
    
    for row in all_data:
        row.icon_color = str_to_color(row.name)
    
    return render_template('index.html', contacts = all_data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = Data(name,email,phone)
        db.session.add(my_data)
        db.session.commit()

        flash("Contact inserted successfully")

        return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()
        flash("Contact updated successfully")

        return redirect(url_for('index'))

@app.route('/delete/<id>/', methods=['POST','GET'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Contact deleted successfully")

    return redirect(url_for('index'))

db.create_all()

if __name__ == "__main__":
    app.run(debug=True)