from flask import render_template, request, Blueprint
from elecshop import db
from elecshop.models import Products

shop = Blueprint("shop", __name__)


@shop.route("/")
@shop.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    products = Products.query.paginate(page=page, per_page=5)
    # products= Products.query.all()

    return render_template("/home.html", title="Dashboard", products=products)
