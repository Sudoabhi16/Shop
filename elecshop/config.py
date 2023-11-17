import os


class Config:
    SECRET_KEY = "02207f7dd889ad65fe1ab14e5a74a44d"
    SQLALCHEMY_DATABASE_URI = "sqlite:///shop.db"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "deliveryallrounder@gmail.com"
    # os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = "pgkjcwgsfrneuvcv"
    os.environ.get("EMAIL_PASS")
