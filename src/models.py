from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from typing import List
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    ID: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(18), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(18), nullable=False)
    firstname: Mapped[str] = mapped_column(String(18), nullable=False)
    lastname: Mapped[str] = mapped_column(String(18), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    date_creation: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    posts: Mapped[List["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    media: Mapped[List["Media"]] = relationship(back_populates="uploader", cascade="all, delete-orphan")
    following: Mapped[List["Follower"]] = relationship(foreign_keys="[Follower.user_from_id]", back_populates="user_from", cascade="all, delete-orphan")
    followers: Mapped[List["Follower"]] = relationship(foreign_keys="[Follower.user_to_id]", back_populates="user_to", cascade="all, delete-orphan")

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

    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post", cascade="all, delete-orphan")
    media: Mapped[List["Media"]] = relationship(back_populates="post", cascade="all, delete-orphan")

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

    uploader: Mapped["User"] = relationship(back_populates="media")
    post: Mapped["Post"] = relationship(back_populates="media")

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
    
    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")

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

    user_from: Mapped["User"] = relationship(foreign_keys=[user_from_id], back_populates="following")
    user_to: Mapped["User"] = relationship(foreign_keys=[user_to_id], back_populates="followers")

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }