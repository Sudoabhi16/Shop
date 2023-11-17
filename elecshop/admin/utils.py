import os
import secrets
from elecshop.models import Types, Products
from flask import current_app
from PIL import Image
from sqlalchemy.orm import load_only


def save_picture(form_picture, image_of):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    if image_of == "Customer":
        picture_path = os.path.join(
            current_app.root_path, "static/profile_pics", picture_fn
        )
    elif image_of == "Product":
        picture_path = os.path.join(
            current_app.root_path, "static/products_pics", picture_fn
        )

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def get_product(product_id):
    return Products.query.filter_by(id=product_id).first()


def product_type_list():
    return Types.query.all()


def get_product_type(type_id):
    return Types.query.filter_by(id=type_id).first()


def get_product_type_id(type):
    product_type = Types.query.filter_by(product_type=type).first()
    return product_type.id
