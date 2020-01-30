import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from zimmerman import create_app
from zimmerman.extensions import db

# Import blueprint
from zimmerman.api import main_bp

# Create the application in development api.
# We obviously want to change this to 'prod' in deployment.
app = create_app("prod")

# Register main blueprint from API
app.register_blueprint(main_bp)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command("db", MigrateCommand)

@manager.command
def run():
    app.run()

# Add Create Admin

@manager.command
def test():
    """ Runs Unit Tests """
    tests = unittest.TestLoader().discover("zimmerman/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


if __name__ == "__main__":
    manager.run()
