from ...utils.databases import SQLDB
from ..schemas.user import User
from pydantic import ValidationError
from fastapi import HTTPException
from pydantic import EmailStr, ValidationError
from ..schemas.user import User


class DatabaseManager:
    def __init__(self, user, password, host, port, dbname, models):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dbname = dbname
        self.models = models

    def get_db(self):
        db = SQLDB(user=self.user,
                   password=self.password,
                   host=self.host,
                   port=self.port,
                   dbname=self.dbname,
                   models=self.models)
        try:
            yield db
        finally:
            db.conn.close()

    def validate_User(self, name: str, email: str):
        try:
            user = User(name=name, email=email)
        except ValidationError as e:
            for error in e.errors():
                if error['loc'][0] == 'email':
                    raise ValueError(f"Email error: {error['msg']}") from None
                elif error['loc'][0] == 'name':
                    raise ValueError(f"Name error: {error['msg']}") from None
