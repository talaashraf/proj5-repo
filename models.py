from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey, LargeBinary
from database import metadata, engine
from sqlalchemy import DateTime
from datetime import datetime

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
)

skills = Table(
    "skills",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("skill_name", String(100), nullable=False, unique=True),
)

user_skills = Table(
    "user_skills",
    metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.id"), primary_key=True),
)

courses = Table(
    "courses",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("course_name", String(200), nullable=False),
    Column("description", Text, nullable=False),
)

embeddings = Table(
    "embeddings",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), nullable=False),
    Column("embedding", LargeBinary, nullable=False),
)

recommendation_logs = Table(
    "recommendation_logs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("course_id", Integer, ForeignKey("courses.id"), nullable=False),
    Column("score", String(50)),
    Column("created_at", DateTime, default=datetime.utcnow),
)

metadata.create_all(engine)

print("Tables created successfully!")