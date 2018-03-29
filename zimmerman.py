from app import app, db
from models import *
from views import *


def create_tables():
    db.database.create_tables([User], safe=True)


if __name__=='__main__':
    create_tables()
    app.run()
