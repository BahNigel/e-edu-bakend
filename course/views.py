from rest_framework import generics
from .models import Course, CourseEnrollment, CourseMaterial, CourseTimetable
from .serializers import CourseEnrollmentSerializer, CourseMaterialSerializer, CourseSerializer, CourseTimetableSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

class CourseListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        # Filter courses by the current logged-in user
        return Course.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save the logged-in user as the owner of the course
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        # Pass the request context to the serializer
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class CourseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer



class CourseEnrollmentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CourseEnrollment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        course_id = self.request.data.get('course_id')
        if not course_id:
            return Response({'course_id': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'course_id': ['Invalid course ID.']}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(user=self.request.user, course=course)

class CourseEnrollmentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CourseEnrollment.objects.filter(user=self.request.user)

class EnrollmentCheckAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, course_id):
        is_enrolled = CourseEnrollment.objects.filter(user=request.user, course_id=course_id).exists()
        return Response({'is_enrolled': is_enrolled})

class EnrolledCoursesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        enrollments = CourseEnrollment.objects.filter(user=request.user)
        courses = [enrollment.course for enrollment in enrollments]
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    
    
class CourseTimetableListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request, *args, **kwargs):
        course_id = request.query_params.get('course')
        if course_id:
            timetables = CourseTimetable.objects.filter(course_id=course_id)
            serializer = CourseTimetableSerializer(timetables, many=True)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Course ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        course = Course.objects.filter(id=data.get('course')).first() 
        week_number = data.get('weekNumber')
        monday = data.get('monday', [])
        tuesday = data.get('tuesday', [])
        wednesday = data.get('wednesday', [])
        thursday = data.get('thursday', [])
        friday = data.get('friday', [])
        saturday = data.get('saturday', [])
        sunday = data.get('sunday', [])
        print(course)
        print(week_number)
        print(monday)
        print(tuesday)
        print(wednesday)
        print(thursday)
        print(friday)
        print(saturday)
        print(sunday)

        # Perform validation as needed

        # Save the course timetable
        course_timetable = CourseTimetable.objects.create(
            course=course,
            week_number=week_number,
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            sunday=sunday
        )
        
        serializer = CourseTimetableSerializer(course_timetable)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CourseTimetableRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseTimetable.objects.all()
    serializer_class = CourseTimetableSerializer
    permission_classes = [IsAuthenticated]

class CourseTimetableAPIView(generics.ListAPIView):
    serializer_class = CourseTimetableSerializer

    def get_queryset(self):
        course_id = self.request.query_params.get('course')
        week_number = self.request.query_params.get('week_number')

        # Perform filtering based on provided parameters
        queryset = CourseTimetable.objects.filter(course_id=course_id, week_number=week_number)
        return queryset
    

class CourseMaterialListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CourseMaterialSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs['courseId']
        return CourseMaterial.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs['courseId']
        course = Course.objects.filter(id=course_id).first()
        if course:
            serializer.save(course=course)
        else:
            raise serializers.ValidationError("Course not found")

class CourseMaterialRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        matetia = CourseMaterial.objects.filter(id=pk).first()
        serializers = CourseMaterialSerializer(matetia)
        print(serializers.data)
        return Response(serializers.data)
    
    def put(self, request, pk):
        matetia = CourseMaterial.objects.filter(id=pk).first()
        print(request.data)
        course = Course.objects.filter(id=(request.data.get('course_id'))).first()
        matetia.course = course
        matetia.title = request.data.get('title')
        matetia.description = request.data.get('description')
        matetia.type = request.data.get('type')
        matetia.file = request.data.get('file')
        matetia.save()
        serializers = CourseMaterialSerializer(matetia)
        print(serializers.data)
        return Response(serializers.data)
    
    def delete(self, request, pk):
        matetia = CourseMaterial.objects.filter(id=pk).first()
        matetia.delete()
        return Response({'message': "data deleted"})
    