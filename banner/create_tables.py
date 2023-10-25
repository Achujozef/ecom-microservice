from app import db  # Import your SQLAlchemy instance
from flask_script import Manager

manager = Manager()

@manager.command
def create_tables():
    db.create_all()

if __name__ == '__main__':
    manager.run()
