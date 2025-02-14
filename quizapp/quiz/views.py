from django.shortcuts import render

from .database import SessionLocal
from .models import Quiz


def home(request):
    session = SessionLocal()
    quizzes = session.query(Quiz).all()
    session.close()
    
    return render(request, "quiz/home.html", {"quizzes": quizzes})
