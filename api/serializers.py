from django.db.models import Avg
from rest_framework import serializers
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from portal.models import Student, Subject, Mark


class MarkSerializer(serializers.Serializer):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    value = serializers.IntegerField()
    student = serializers.CharField()
    subject = serializers.CharField()

    def create(self, validated_data):
        student_name = validated_data.pop('student')
        subject_name = validated_data.pop('subject')
        student = Student.objects.get(name=student_name)
        subject = Subject.objects.get(name=subject_name)
        mark = Mark.objects.create(student=student, subject=subject, **validated_data)
        return mark

    def update(self, instance, validated_data):
        student_name = validated_data.pop('student', None)
        subject_name = validated_data.pop('subject', None)
        if student_name:
            instance.student = Student.objects.get(name=student_name)
        if subject_name:
            instance.subject = Subject.objects.get(name=subject_name)
        instance.value = validated_data.get('value', instance.value)
        instance.save()
        return instance



class StudentSubjectAverageMarkSerializer(serializers.Serializer):
    
    class Meta:
        model = Mark
        fields = ('student_name', 'subject_name', 'group_name', 'average_mark')

    def to_representation(self, instance):
        print(instance)
        marks = Mark.objects.filter(student__name=instance.student.name, subject__name=instance.subject.name)
        group_marks = Mark.objects.raw("""
                                        SELECT * 
                                        FROM portal_mark 
                                        INNER JOIN portal_student ON portal_mark.student_id = portal_student.id 
                                        INNER JOIN portal_group ON portal_student.group_id = portal_group.id 
                                        INNER JOIN portal_subject ON portal_mark.subject_id = portal_subject.id 
                                        WHERE portal_group.name = 'group_name' AND portal_subject.name = %s", [lname]
                                        """)
        group_name = instance.student.group.name
        if marks:
            average_mark = marks.aggregate(Avg('value'))['value__avg']
            return {
                'student_name': instance.student.name,
                'subject_name': instance.subject.name,
                'group_name': group_name,
                'average_mark': round(average_mark, 2)
            }
            
        elif group_marks:
            average_mark = group_marks.aggregate(Avg('value'))['value__avg']
            return {
                'subject_name': instance.subject.name,
                'group_name': group_name,
                'average_mark': round(average_mark, 2)
            }
            
        print('No data found')


