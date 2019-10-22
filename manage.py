import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from zimmerman.main import create_app
from zimmerman.main.extensions import db

# Models
from zimmerman.main.model import user

# Import blueprint
from zimmerman import main_bp

# Create the application in development mode.
# We obviously want to change this to 'prod' in deployment.
app = create_app('dev')

# Register main blueprint from Zimmerman
app.register_blueprint(main_bp)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run()

@manager.command
def test():
    """ Runs Unit Tests """
    tests = unittest.TestLoader().discover('zimmerman/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1

if __name__ == '__main__':
    manager.run()
