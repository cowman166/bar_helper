from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from model import connect_to_db

app = Flask(__name__)

# favorites = db.Table('favorites',       #make into a table in model.py
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
# )

# login_manager = LoginManager()
# login_manager.init_app(app)
#come back for research

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
app.secret_key = "dev" #make this secret tomoro with trew
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    return redirect(url_for('search'))

@app.route('/search', methods=['POST'])
def search():
    ingredient1 = request.form['ingredient1']
    ingredient2 = request.form['ingredient2']

    recipes = Recipe.query.join(Ingredient).filter(
        Ingredient.name == ingredient1).join(
        Ingredient, Recipe.id == Ingredient.recipe_id).filter(
        Ingredient.name == ingredient2).all()

    return render_template('recipes.html', recipes=recipes)

@app.route('/favorite/<int:recipe_id>', methods=['POST'])
@login_required
def favorite(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe and current_user.is_authenticated:
        if recipe not in current_user.favorites:
            current_user.favorites.append(recipe)
            db.session.commit()
            return 'Recipe favorited successfully!'
    return 'You must be logged in to favorite recipes.'

@app.route('/register', methods = ['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    screen_name = request.form['screen_name']
    profile_pic = request.form['profilepic', '']
    allergies = request.form['allergies', '']

    hashed_password = generate_password_hash(password)

    user = User(username=username, email=email, password=hashed_password, 
                screen_name=screen_name, profile_pic=profile_pic, allergies=allergies)
    db.session.add(user)
    db.session.commit()

    return 'Registration successful!'


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)