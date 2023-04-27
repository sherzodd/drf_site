from django.urls import path
from api.views import StudentSubjectAverageMarkView
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('get_marks/', StudentSubjectAverageMarkView.as_view(), name='get_marks'),
]