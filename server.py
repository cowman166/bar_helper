from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from model import connect_to_db, db, Recipe, Ingredient, User, Allergy
import os

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
# app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search_bar')
def search_bar():
    return render_template("search.html")

@app.route('/search', methods=['POST'])
def search():
    ingredient1 = request.form['ingredient1']
    ingredient2 = request.form['ingredient2']
    ingredient3 = request.form['ingredient3']
    ingredient4 = request.form['ingredient4']
    user_input = {ingredient1.lower(), ingredient2.lower(), ingredient3.lower(), ingredient4.lower()}

    filtered_recipe = set()
    recipes = Recipe.query.all() # [ <Recipe>, <Recipe>, <Recipe>.... ] => <Recipe>.key

    for recipe in recipes:
        recipe_ingredients = set(recipe.key.strip().lower().split(',')) # iterating over all recipes
        if recipe_ingredients.intersection(user_input):
            filtered_recipe.add(recipe)

    return render_template('recipes.html', recipes=filtered_recipe)

@app.route('/favorite/<int:recipe_id>', methods=['POST'])
@login_required
def favorite(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe and current_user.is_authenticated:
        if recipe not in current_user.favorites:
            current_user.favorites.append(recipe)
            db.session.commit()
            return 'Recipe favorited successfully!'
    return redirect("/")

@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.get_by_username(username)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_username"] = user.username
        flash(f"Welcome back, {user.username}!")

    return redirect("/")

@app.route("/login", methods=["GET"])
def login():

    return render_template("login.html")

@app.route("/register_user")
def register_user():
    all_allergies = [allergy.ingredient_name for allergy in Allergy.query.all()]
    return render_template("register.html", all_allergies=all_allergies)

@app.route('/register', methods = ['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    profile_pic = request.form.get('profilepic', '')
    allergies = request.form.get('allergies', '')

    hashed_password = generate_password_hash(password)

    user = User(username=username, email=email, password=hashed_password, 
                profile_pic=profile_pic)
    db.session.add(user)
    db.session.commit()
    if allergies:
        current_boi = User.query.filter(User.username==username).first()
        allergies_list = allergies.strip().split(',')
        for allergy in allergies_list:
            new_allergy = Allergy(user_id = current_boi.id, ingredient_name=allergy)
            db.session.add(new_allergy)
    db.session.commit()
    flash("Account created!")

    return redirect("/")


if __name__ == "__main__":
    app.app_context().push()
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)