from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)

    questions = relationship("Question", back_populates="quiz")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_text = Column(String(500), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))

    quiz = relationship("Quiz", back_populates="questions")