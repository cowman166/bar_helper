from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(128), nullable = False) 
    screen_name = db.Column(db.String(50), nullable = False)
    profile_pic = db.Column(db.String(100))
    allergies = db.Column(db.String(255))
    favorites = db.relationship('Recipe', secondary=favorites, lazy='subquery',
                                backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.screen_name}')"

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True)

    def __repr__(self):
        return f"Recipe('{self.name}')"

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(20))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    def __repr__(self):
        return f"Ingredient('{self.name}', '{self.quantity}')"

@app.route('/search', methods=['POST'])
def search():
    ingredient1 = request.form['ingredient1']
    ingredient2 = request.form['ingredient2']

    # Query recipes that contain both ingredients
    recipes = Recipe.query.join(Ingredient).filter(
        Ingredient.name == ingredient1).join(
        Ingredient, Recipe.id == Ingredient.recipe_id).filter(
        Ingredient.name == ingredient2).all()

    return render_template('recipes.html', recipes=recipes)

@app.route('/favorite/<int:recipe_id>', methods=['POST'])
def favorite(recipe_id):
    user = User.query.get(1) 

    recipe = Recipe.query.get(recipe_id)
    if recipe and user:
        if recipe not in user.favorites:
            user.favorites.append(recipe)
            db.session.commit()

    return 'Recipe favorited successfully!'

@app.route('/register', methods = ['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    screen_name = request.form['screen_name']
    profile_pic = request.form['profilepic', '']
    allergies = request.form['allergies', '']

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password, 
                    screen_name=screen_name, profile_pic=profile_pic, 
                    allergies=allergies)
    
    db.session.add(new_user)
    db.session.commit()
    return "User registered Successfully!"

@app.route('/favorites')
def favorites():
    user = User.query.get(1) 

    return render_template('favorites.html', user=user)

@app.route('/login', methods = ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        cocktail_history = get_cocktail_history(username)
        return "Login Successful!"
    else:
        return "Invalid Username or Password"
    
def get_cocktail_history(username):
    return ["Margarita", "Martini", "Cosmopolitan"]

if __name__ == '__main__':
    app.run(debug = True)
