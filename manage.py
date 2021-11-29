from app import app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app.commands import CreateSuperUserCommand

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
manager.add_command('create_superuser', CreateSuperUserCommand)


if __name__ == '__main__':
    manager.run()