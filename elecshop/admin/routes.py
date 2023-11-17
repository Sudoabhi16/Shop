from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_required, current_user
from elecshop import db
from elecshop.models import User, Products, Types
from elecshop.admin.forms import (
    AddProductTypeForm,
    EditProductTypeForm,
    AddProductForm,
    EditProductForm,
)
from elecshop.admin.utils import (
    save_picture,
    get_product_type_id,
    get_product_type,
    get_product,
)

admin = Blueprint("admin", __name__)


"""
=====================================================================================================================================================================
PRODUCTS
=====================================================================================================================================================================
"""


@login_required
@admin.route("/products", methods=["GET", "POST"])
def products():
    if current_user.user_name == "Admin":
        page = request.args.get("page", 1, type=int)
        products = Products.query.paginate(page=page, per_page=5)
        return render_template(
            "admin/products.html", title="All Products", products=products
        )
    return render_template("404.html")


@login_required
@admin.route("/products/<product_id>", methods=["GET", "POST"])
def product_item(product_id):
    if current_user.user_name == "Admin":
        page = request.args.get("page", 1, type=int)
        users = User.query.paginate(page=page, per_page=5)
        return render_template(
            "admin/product_item.html", title="Product Details", users=users
        )
    return render_template("404.html")


@login_required
@admin.route("/products/add_product", methods=["GET", "POST"])
def add_product():
    if current_user.user_name == "Admin":
        form = AddProductForm()
        if form.validate_on_submit():
            product_type = (form.product_type.data).product_type
            if form.picture.data:
                picture_file = save_picture(form.picture.data, "Product")
                product = Products(
                    product_name=form.productname.data,
                    price=form.price.data,
                    quantity=form.quantity.data,
                    availablity=form.availablity.data,
                    image_file=picture_file,
                    details=form.details.data,
                    product_type=get_product_type_id(product_type),
                )
            else:
                product = Products(
                    product_name=form.productname.data,
                    price=form.price.data,
                    quantity=form.quantity.data,
                    availablity=form.availablity.data,
                    details=form.details.data,
                    product_type=get_product_type_id(product_type),
                )
            db.session.add(product)
            db.session.commit()
            flash(f"Product Added Successfully", "success")
            return redirect(url_for("admin.products"))
        return render_template(
            "admin/add_product.html",
            title="Add Product",
            form=form,
            legend="Add Product",
        )
    return render_template("404.html")


@login_required
@admin.route("/products/<product_id>/edit_product", methods=["GET", "POST"])
def edit_product(product_id):
    if current_user.user_name == "Admin":
        form = EditProductForm()
        product = get_product(product_id)
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data, "Product")
                product.image_file = picture_file
            product_type = (form.product_type.data).product_type
            product.product_name = form.productname.data
            product.price = form.price.data
            product.quantity = form.quantity.data
            product.availablity = form.availablity.data
            product.details = form.details.data
            product.product_type = get_product_type_id(product_type)
            db.session.commit()
            flash(f"Product Updated Successfully", "success")
            return redirect(url_for("admin.products"))
        elif request.method == "GET":
            product_type = get_product_type(product.product_type)

            form.picture.data = product.image_file
            form.productname.data = product.product_name
            form.price.data = product.price
            form.quantity.data = product.quantity
            form.availablity.data = product.availablity
            form.details.data = product.details
            form.product_type.data = product.product_type
        image_file = url_for("static", filename="products_pics/" + product.image_file)
        return render_template(
            "admin/edit_product.html",
            title="Update Product",
            form=form,
            legend="Edit Product",
            image_file=image_file,
        )
    return render_template("404.html")


@login_required
@admin.route("/produts/<product_id>/delete_product", methods=["GET", "POST"])
def delete_product(product_id):
    if current_user.user_name == "Admin":
        product = get_product(product_id)
        db.session.delete(product)
        db.session.commit()
        flash(f"Product  Deleted Successfully", "danger")
        return redirect(url_for("admin.products"))
    return render_template("404.html")


"""
=====================================================================================================================================================================
PRODUCT TYPE
=====================================================================================================================================================================
"""


@login_required
@admin.route("/product_type", methods=["GET", "POST"])
def product_type():
    if current_user.user_name == "Admin":
        page = request.args.get("page", 1, type=int)
        types = Types.query.paginate(page=page, per_page=5)
        return render_template(
            "admin/product_type.html", title="Product Type", types=types
        )
    return render_template("404.html")


@login_required
@admin.route("/product_type/new", methods=["GET", "POST"])
def add_product_type():
    if current_user.user_name == "Admin":
        form = AddProductTypeForm()
        if form.validate_on_submit():
            type = Types(product_type=form.product_type_name.data)
            db.session.add(type)
            db.session.commit()
            flash(f"Product Type Added Successfully", "success")
            return redirect(url_for("admin.product_type"))
        return render_template(
            "admin/add_product_type.html",
            title="Adding Product Type",
            form=form,
            legend="New Product Type",
        )
    return render_template("404.html")


@login_required
@admin.route("/product_type/<type_id>/edit_product_type", methods=["GET", "POST"])
def edit_product_type(type_id):
    if current_user.user_name == "Admin":
        form = EditProductTypeForm()
        type = get_product_type(type_id)
        if form.validate_on_submit():

            type.product_type = form.product_type_name.data
            db.session.commit()
            flash(f"Product Type Updated Successfully", "success")
            return redirect(url_for("admin.product_type"))
        elif request.method == "GET":
            form.product_type_name.data = type.product_type
        return render_template(
            "admin/add_product_type.html",
            title="Adding Product Type",
            form=form,
            legend="Edit Product Type",
        )
    return render_template("404.html")


@admin.route("/product_type/<type_id>/delete_type", methods=["GET", "POST"])
@login_required
def delete_type(type_id):
    type = get_product_type(type_id)
    if current_user.user_name == "Admin":
        db.session.delete(type)
        db.session.commit()
        flash(f"Product Type Deleted Successfully", "danger")
        return redirect(url_for("admin.product_type"))
    return render_template("404.html")


"""
=====================================================================================================================================================================
CUSTOMERS
=====================================================================================================================================================================
"""


@login_required
@admin.route("/customers", methods=["GET", "POST"])
def customers():
    if current_user.user_name == "Admin":
        page = request.args.get("page", 1, type=int)
        users = User.query.paginate(page=page, per_page=5)
        return render_template(
            "admin/customers.html", title="Customer Details", users=users
        )
    return render_template("404.html")
