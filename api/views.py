from django.db.models import Avg
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from portal.models import Student, Subject, Mark
from . import serializers

class StudentSubjectAverageMarkView(APIView):

    def get(self, request):
        student_name = request.GET.get('student_name')
        subject_name = request.GET.get('subject_name')
        marks = Mark.objects.filter(student__name=student_name, subject__name=subject_name)
        serializer = serializers.StudentSubjectAverageMarkSerializer(marks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.MarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, student_name, subject_name):
        serializer = serializers.MarkSerializer(data=request.data)
        mark = serializer.save(student_name=student_name, subject_name=subject_name)
        response_data = {
            'id': mark.id,
            'student_name': student_name,
            'subject_name': subject_name,
            'value': mark.value
        }
        return Response(response_data, status=200)

    def delete(self, request, student_name, subject_name):
        mark_id = request.data.get('id')
        mark = Mark.objects.get(id=mark_id, student__name=student_name, subject__name=subject_name)
        mark.delete()
        return Response({'message': f'Mark with id {mark_id} for student {student_name} and subject {subject_name} has been deleted.'}, status=200)
