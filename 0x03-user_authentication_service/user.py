#!/usr/bin/env python3
"""
This module defines the SQLAlchemy ORM model for the "users" table.

The User class represents a user entity with attributes such as email,
hashed password, session ID, and password reset token.
It is mapped to the "users" table in the database
and provides a structure for user authentication and session management.
"""

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """
     Represents a user in the database with authentication details.

     This class defines the structure of the "users" table,
     including columns for the user's ID, email, hashed password,
     session ID, and password reset token. It is mapped to the "users"
     table in the database using SQLAlchemy ORM.

     Attributes:
         id (int): The unique identifier for the user (primary key).
         email (str): The user's email address, which cannot be null.
         hashed_password (str): The user's hashed password,
            which cannot be null.
         session_id (str, optional): A session ID for the user, can be null.
         reset_token (str, optional): A token for resetting the
            user's password, can be null.
     """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
