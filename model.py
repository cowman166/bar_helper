from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(128), nullable = False) 
    profile_pic = db.Column(db.String(100))

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter(User.username == username).first()

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

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
    def __repr__(self):
        return f"Recipe('{self.name}', '{self.description}', '{self.key}, '{self.served}', '{self.ingredients})"
    
    @classmethod
    def create(cls, name, description, served, ingredients, key):

       return cls(name=name, description=description, served=served, ingredients=ingredients, key=key)

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