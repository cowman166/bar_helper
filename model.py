from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(128), nullable = False) 
    screen_name = db.Column(db.String(50), nullable = False)
    profile_pic = db.Column(db.String(100))
    allergies = db.Column(db.String(255))
    history = db.Column(db.Text)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.screen_name}')"

@app.route('/register', methods = ['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    screen_name = request.form['screen_name']
    profile_pic = request.form['profilepic', '']
    allergies = request.form['allergies', '']
    history = request.form['history', '']

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password, 
                    screen_name=screen_name, profile_pic=profile_pic, 
                    allergies=allergies, history=history)
    
    db.session.add(new_user)
    db.session.commit()
    return "User registered Successfully!"

app.route('/login', methods = ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return "Login Successful!"
    else:
        return "Invalid Username or Password"
    
if __name__ == '__main__':
    app.run(debug = True)
