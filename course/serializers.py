from rest_framework import serializers
from .models import Course, CourseEnrollment, CourseMaterial, CourseTimetable

class CourseSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'duration', 'course_image', 'creator']

    def get_creator(self, obj):
        # Check if the logged-in user is the creator of the course
        request = self.context.get('request')
        if request and request.user == obj.user:
            return True
        return False
    

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CourseEnrollment
        fields = ['id', 'user', 'course', 'course_id', 'enrolled_at']
        read_only_fields = ['user', 'course', 'enrolled_at']

    def create(self, validated_data):
        course_id = validated_data.pop('course_id')
        course = Course.objects.get(id=course_id)
        enrollment = CourseEnrollment.objects.create(user=validated_data['user'], course=course)
        return enrollment
    
class CourseTimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTimetable
        fields = '__all__'


class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = ['id', 'title', 'description', 'file', 'type', 'course']
        read_only_fields = ['id', 'course']

    def to_representation(self, instance):
        """Convert `file` to URL in response."""
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if request is not None and instance.file:
            ret['file'] = request.build_absolute_uri(instance.file.url)
        return ret