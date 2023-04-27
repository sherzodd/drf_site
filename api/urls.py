from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    path('average-mark/', views.StudentSubjectAverageMarkView.as_view()),
    path('average-mark/<str:student_name>/<str:subject_name>/', views.StudentSubjectAverageMarkView.as_view()),
    path('api-token-auth/', obtain_jwt_token),
    ]


urlpatterns = format_suffix_patterns(urlpatterns)
