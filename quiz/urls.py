from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_quiz, name='render-quiz'),
    path('result', views.render_result, name='render-result'),
    path('initial-quiz', views.quiz, name='quiz'),
    path('shuffle-quiz', views.shuffle, name='shuffle'),
    path('reset-quiz', views.reset, name='reset'),
    path('filter-quiz', views.filter, name='filter'),
]