from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False) 
    profile_pic = db.Column(db.String(100))
    
    favorites = relationship('Favorite', back_populates='user')

    def add_to_favorites(self, recipe):
        """Add a recipe to the user's favorites."""
        if recipe not in self.favorites:
            favorite = Favorite(user=self, recipe=recipe)
            db.session.add(favorite)
            db.session.commit()

    def remove_from_favorites(self, recipe):
        """Remove a recipe from the user's favorites."""
        favorite = Favorite.query.filter_by(user=self, recipe=recipe).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()

    def get_favorite_cocktails(self):
        """Get all favorite cocktails for the user."""
        print(self.favorites)
        return [favorite.recipe for favorite in self.favorites]

class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)

    user = relationship('User', back_populates='favorites')
    recipe = relationship('Recipe')  # Assuming you have a Recipe model


    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter(User.username == username).first()

    def __repr__(self):
        return f"Favorite('{self.user_id}', '{self.recipe_id}')"

class Allergy(db.Model):
    __tablename__ = "allergies"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ingredient_name = db.Column(db.String, db.ForeignKey('ingredients.name'), nullable=False)
    user = db.relationship('User', backref=db.backref('allergies', lazy=True))
    ingredient = db.relationship('Ingredient', backref=db.backref('allergies', lazy=True))

    def __repr__(self):
        return f"Allergy('{self.user_id}', '{self.ingredient_name}')"

class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    served = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    key = db.Column(db.Text)
    pic = db.Column(db.String)
    def __repr__(self):
        return f"Recipe('{self.name}', '{self.description}', '{self.key}, '{self.served}', '{self.ingredients}, '{self.pic}')"
    
    @classmethod
    def create(cls, name, description, served, ingredients, key, pic):

       return cls(name=name, description=description, served=served, ingredients=ingredients, key=key, pic=pic)

class Ingredient(db.Model):
    __tablename__ = "ingredients"
    name = db.Column(db.String(100), nullable=False, primary_key=True)

    def __repr__(self):
        return f"Ingredient('{self.name}')"

    @classmethod
    def create(cls, name):

       return cls(name=name)


def connect_to_db(app, db_name = 'cocktails'):
    app.config["SQLALCHEMY_DATABASE_URI"]=f"postgresql:///{db_name}"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from server import app
    app.app_context().push()
    connect_to_db(app)