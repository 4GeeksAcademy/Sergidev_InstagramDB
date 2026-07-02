from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    ID: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(18), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(18), nullable=False)
    firstname: Mapped[str] = mapped_column(String(18), nullable=False)
    lastname: Mapped[str] = mapped_column(String(18), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    date_creation: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def serialize(self):
        return {
            "ID": self.ID,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "date_creation": self.date_creation
        }


class Post(db.Model):
    ID: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.ID'), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def serialize(self):
        return {
            "ID": self.ID,
            "user_id": self.user_id,
            "date": self.date
        }


class Media(db.Model):
    ID: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.ID'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.ID'), nullable=False)
    type: Mapped[str] = mapped_column(String(18), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    url: Mapped[str] = mapped_column(String(256), nullable=False)

    def serialize(self):
        return {
            "ID": self.ID,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "type": self.type,
            "date": self.date,
            "url": self.url
        }


class Comment(db.Model):   
    ID: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.ID'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.ID'), nullable=False)
    comment_text: Mapped[str] = mapped_column(String(1024), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    def serialize(self):
        return {
            "ID": self.ID,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "comment_text": self.comment_text,
            "date": self.date
        }


class Follower(db.Model):
    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.ID'), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.ID'), primary_key=True)

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }