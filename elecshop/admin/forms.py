from email.policy import default
from unicodedata import decimal
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    SubmitField,
    IntegerField,
    BooleanField,
    TextAreaField,
    DecimalField,
    SelectField,
)
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, NumberRange, ValidationError
from elecshop.models import Products, Types, User
from flask_login import current_user
from elecshop.admin.utils import product_type_list


"""
Products Forms
"""


class AddProductForm(FlaskForm):
    productname = StringField(
        "Name of the Product", validators=[DataRequired(), Length(min=1, max=20)]
    )
    price = DecimalField(
        "Price", validators=[DataRequired(), NumberRange(min=0, max=None)]
    )
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    availablity = BooleanField("Tick if available")
    product_type = QuerySelectField(
        query_factory=product_type_list, allow_blank=False, get_label="product_type"
    )
    picture = FileField("", validators=[FileAllowed(["jpg", "png"])])
    details = TextAreaField("Specification", validators=[DataRequired()])
    submit = SubmitField("Add")


class EditProductForm(FlaskForm):
    productname = StringField(
        "Name of the Product", validators=[DataRequired(), Length(min=1, max=20)]
    )
    price = DecimalField(
        "Price", validators=[DataRequired(), NumberRange(min=0, max=None)]
    )
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    availablity = BooleanField("Tick if available")
    product_type = QuerySelectField(
        query_factory=product_type_list, allow_blank=False, get_label="product_type"
    )
    picture = FileField("", validators=[FileAllowed(["jpg", "png"])])
    details = TextAreaField("Specification", validators=[DataRequired()])
    submit = SubmitField("Update")


class DeleteProductForm(FlaskForm):
    pass


"""
Product Type Forms
"""


class AddProductTypeForm(FlaskForm):
    product_type_name = StringField(
        "Product Type", validators=[DataRequired(), Length(min=1, max=20)]
    )
    submit = SubmitField("Add")


class EditProductTypeForm(FlaskForm):
    product_type_name = StringField(
        "Product Type", validators=[DataRequired(), Length(min=1, max=20)]
    )
    submit = SubmitField("Update")
