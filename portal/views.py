from django.db.models import Avg
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from portal.models import Student, Subject, Mark

class StudentSubjectAverageMarkView(APIView):
    template_name = 'get_marks.html'

    def get(self, request):
        student_name = request.GET.get('student_name')
        subject_name = request.GET.get('subject_name')
        if student_name:
            student = Student.objects.get(name=student_name)
            group_name = student.group.name

        if student_name and subject_name:
            marks = Mark.objects.filter(student__name=student_name, subject__name=subject_name)
            average_mark = marks.aggregate(Avg('value'))['value__avg']
            response_data = {
                'student_name': student_name,
                'subject_name': subject_name,
                'group_name' : group_name,
                'average_mark': round(average_mark, 2)
            }
            return render(request, self.template_name, {'response_data': response_data})
        else:
            return render(request, self.template_name)


    def post(self, request, student_name, subject_name):
        student = Student.objects.get(name=student_name)
        subject = Subject.objects.get(name=subject_name)
        value = request.data.get('value')
        mark = Mark.objects.create(student=student, subject=subject, value=value)
        response_data = {
            'id': mark.id,
            'student_name': student_name,
            'subject_name': subject_name,
            'value': value
        }
        return Response(response_data, status=201)

    def put(self, request, student_name, subject_name):
        mark_id = request.data.get('id')
        mark = Mark.objects.get(id=mark_id, student__name=student_name, subject__name=subject_name)
        value = request.data.get('value')
        mark.value = value
        mark.save()
        response_data = {
            'id': mark.id,
            'student_name': student_name,
            'subject_name': subject_name,
            'value': value
        }
        return Response(response_data, status=200)

    def delete(self, request, student_name, subject_name):
        mark_id = request.data.get('id')
        mark = Mark.objects.get(id=mark_id, student__name=student_name, subject__name=subject_name)
        mark.delete()
        return Response({'message': f'Mark with id {mark_id} for student {student_name} and subject {subject_name} has been deleted.'}, status=200)
    
    

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('get_marks')

    def get_success_url(self):
        return self.success_url
    
    