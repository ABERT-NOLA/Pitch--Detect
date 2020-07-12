from  flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from app import app
manager = Manager(app)
manager.add_command('db',MigrateCommand)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
if __name__ == "__main__":
    manager.run() 