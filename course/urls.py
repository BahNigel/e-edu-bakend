from django.urls import path
from .views import CourseEnrollmentListCreateAPIView, CourseEnrollmentRetrieveUpdateDestroyAPIView, CourseListCreateAPIView, CourseMaterialListCreateAPIView, CourseMaterialRetrieveUpdateDestroyAPIView, CourseRetrieveUpdateDestroyAPIView, CourseTimetableAPIView, CourseTimetableListCreateAPIView, CourseTimetableRetrieveUpdateDestroyAPIView, EnrolledCoursesAPIView, EnrollmentCheckAPIView

urlpatterns = [
    path('', CourseListCreateAPIView.as_view(), name='course-list-create'),
    path('<int:pk>/', CourseRetrieveUpdateDestroyAPIView.as_view(), name='course-detail'),
    path('enrollments/', CourseEnrollmentListCreateAPIView.as_view(), name='enrollment-list-create'),
    path('enrollments/<int:pk>/', CourseEnrollmentRetrieveUpdateDestroyAPIView.as_view(), name='enrollment-detail'),
    path('enrollments/check/<int:course_id>/', EnrollmentCheckAPIView.as_view(), name='enrollment-check'),
    path('timetables/', CourseTimetableListCreateAPIView.as_view(), name='course-timetable-list-create'),
    path('timetables/<int:pk>/', CourseTimetableRetrieveUpdateDestroyAPIView.as_view(), name='course-timetable-detail'),
    path('courses/timetables/', CourseTimetableAPIView.as_view(), name='course_timetables'),
    path('<int:courseId>/materials/', CourseMaterialListCreateAPIView.as_view(), name='material-list-create'),
    path('materials/<int:pk>/', CourseMaterialRetrieveUpdateDestroyAPIView.as_view(), name='material-retrieve-update-destroy'),
    path('enrollments/my-courses/', EnrolledCoursesAPIView.as_view(), name='enrolled-courses'),
]
