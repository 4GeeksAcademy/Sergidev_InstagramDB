from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    ID: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(18), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(18), unique=False, nullable=False)
    lastname: Mapped[str] = mapped_column(String(18), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)


    def serialize(self):
        return {
            "ID": self.id,
            "email": self.email,

        }
