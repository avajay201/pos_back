from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from .models import Order, Device, Course, Teacher



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'profile_pic', 'price', 'created_at')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'name', 'email', 'phone', 'profile_pic', 'created_at')


class RegisterDeviceAPIView(APIView):
    def post(self, request):
        mac = request.data.get('mac_address')
        if not mac:
            return Response({'error': 'Mac address is required.'}, status=status.HTTP_400_BAD_REQUEST)
        Device.objects.get_or_create(mac_address=mac)
        return Response(status=status.HTTP_200_OK)


class CourseAPIView(APIView):
    def get(self, request, t_id):
        if not t_id:
            return Response({'error': 'Teacher ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        courses = Course.objects.filter(teacher=t_id)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeachersAPIView(APIView):
    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterOrderAPIView(APIView):
    def post(self, request):
        coursesData = request.data.get('courses')
        if not coursesData:
            return Response({'error': 'Courses are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            device = Device.objects.get(mac_address=request.data['device'])
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=status.HTTP_400_BAD_REQUEST)

        courses_ids = list(list(crs.keys())[0] for crs in coursesData)
        try:
            courses = Course.objects.filter(id__in=courses_ids)
        except Course.DoesNotExist:
            return Response({'error': 'One or more courses not found'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = 0
        for crs in coursesData:
            course_id = list(crs.keys())[0]
            course = Course.objects.get(id=course_id)
            total_price += course.price * crs[course_id]

        order = Order.objects.create(device=device, buyer=request.data['buyer'], buyer_email=request.data['buyer_email'], buyer_phone=request.data['buyer_phone'], total_price=total_price)
        order.courses.set(courses)
        order_data = {
            'buyer': order.buyer,
            'buyer_email': order.buyer_email,
            'buyer_phone': order.buyer_phone,
            'total_price': order.total_price,
            'courses': [course.title for course in order.courses.all()],
            'ordered_at': order.ordered_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        return Response(order_data, status=status.HTTP_201_CREATED)
