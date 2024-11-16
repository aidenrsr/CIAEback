from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

'''
for db models, import "from db import db"
and use (db.Model) for class

for application, "from db import db, init_db"
init_db(app) to initialize db in app
'''