from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(128), nullable = False) 
    screen_name = db.Column(db.String(50), nullable = False) #If user wants to have diff screen name
    profile_pic = db.Column(db.String(100))
    # allergies = db.Column(db.String(255)) make its own table
    # favorites = db.relationship('Recipe', secondary=favorites, lazy='subquery',
    #                             backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.screen_name}')"

class Allergies(db.Model):
    __tablename__ = "allergies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    user = db.relationship("User", back_populates="allergies")
    def __repr__(self):
        return f"Allergies('{self.name}', '{self.description}')"
        
class Quantity(db.Model):
    __tablename__ = "quantity"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.text, nullable=False)
    type = db.relationship('Type', backref='quantity' )

    def __repr__(self):
        return f"Quantity('{self.name}', '{self.description}', '{self.type}')"
    
class Recipe(db.Model):
    __tablename__ = "recipe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True)
    
    def __repr__(self):
        return f"Recipe('{self.name}', '{self.description}', '{self.ingredients})"

class Ingredient(db.Model):
    __tablename__ = "ingredient"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(20))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    def __repr__(self):
        return f"Ingredient('{self.name}', '{self.quantity}')"

def connect_to_db(app, db_name = 'cocktails'):
    app.config["SQLACHEMY_DATABASE_URI"]=f"postgresql:///{db_name}"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from server import app
    connect_to_db(app)