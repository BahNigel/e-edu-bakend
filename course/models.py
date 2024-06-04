from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=50)
    course_image = models.ImageField(upload_to='course_images/', default='default_image.jpg')

    def __str__(self):
        return self.title


class CourseEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
    
    
class CourseTimetable(models.Model):
    DAYS_OF_WEEK = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetable')
    week_number = models.PositiveIntegerField()
    monday = models.JSONField(default=list)  # Array of start and end times for Monday
    tuesday = models.JSONField(default=list)  # Array of start and end times for Tuesday
    wednesday = models.JSONField(default=list)  # Array of start and end times for Wednesday
    thursday = models.JSONField(default=list)  # Array of start and end times for Thursday
    friday = models.JSONField(default=list)  # Array of start and end times for Friday
    saturday = models.JSONField(default=list)  # Array of start and end times for Saturday
    sunday = models.JSONField(default=list)  # Array of start and end times for Sunday

    def __str__(self):
        return f"Timetable for {self.course.title}"

class CourseMaterial(models.Model):
    MATERIAL_TYPES = [
        ('video', 'Video'),
        ('file', 'File'),
        ('audio', 'Audio'),
        ('image', 'Image'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_material')
    title = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=10, choices=MATERIAL_TYPES)
    file = models.FileField(upload_to='course_materials/%Y/%m/%d/')