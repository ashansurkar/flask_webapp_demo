from sqlalchemy import *
from flask_login import UserMixin
from practice import db_session, Base, engine, login_manager, bcrypt
import uuid

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(Base,UserMixin):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=uuid.uuid4().hex)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

    def set_password(self,password):
        self.password = bcrypt.generate_password_hash(
            password
        ).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.check_password_hash(self.password,password)

    def __str__(self):
        return f'{self.username}'

Base.metadata.create_all(engine)
