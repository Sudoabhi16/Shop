from elecshop import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as TJSS
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20))
    contact_num = db.Column(db.String(13), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(20), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = TJSS(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"userid": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = TJSS(current_app.config["SECRET_KEY"])
        try:
            userid = s.loads(token)["userid"]
        except:
            return None
        return User.query.get(userid)

    def __repr__(self) -> str:
        return f"User('{self.user_name}', '{self.first_name}', '{self.last_name}', '{self.contact_num}', '{self.email}', '{self.image_file}' )"


class Types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_type = db.Column(db.String(20), unique=True, nullable=False)
    product = db.relationship("Products", backref="type", lazy=True)
    # db.Column(db.Integer, db.ForeignKey('products.id'), nullable = False)

    def __repr__(self) -> str:
        return f"User('{self.id}', '{self.product_type}' )"


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(20), unique=True, nullable=False)
    price = db.Column(db.Numeric(), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    availablity = db.Column(db.Boolean, default=False, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default_product.png")
    details = db.Column(db.Text, nullable=False)
    product_type = db.Column(db.Integer, db.ForeignKey("types.id"), nullable=False)
    # db.relationship('ProductType', backref = 'Type', lazy = True)

    def __repr__(self) -> str:
        return f"User('{self.product_name}', '{self.price}', '{self.quantity}', '{self.availablity}', '{self.image_file}', '{self.details}', {self.product_type}' )"
