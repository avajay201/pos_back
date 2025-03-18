from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from .models import Order, Device, Course, Teacher, Subject
from datetime import datetime
import json



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'profile_pic', 'price', 'created_at')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'name', 'email', 'phone', 'profile_pic', 'created_at')


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name', 'description')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['stored_ids'] = json.loads(instance.stored_ids)
        return representation


class RegisterDeviceAPIView(APIView):
    def post(self, request):
        android_id = request.data.get('android_id')
        if not android_id:
            return Response({'error': 'Android ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        Device.objects.get_or_create(android_id=android_id)
        return Response(status=status.HTTP_200_OK)


class CourseAPIView(APIView):
    def get(self, request, t_id):
        if not t_id:
            return Response({'error': 'Teacher ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        courses = Course.objects.filter(teacher=t_id)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeachersAPIView(APIView):
    def get(self, request, s_id):
        teachers = Teacher.objects.filter(subject=s_id)
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterOrderAPIView(APIView):
    def post(self, request):
        courses = str(request.data.get('courses'))
        if not courses:
            return Response({'error': 'Courses are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            device = Device.objects.get(android_id=request.data['device'])
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     courses = Course.objects.filter(id__in=courses)
        # except Course.DoesNotExist:
        #     return Response({'error': 'One or more courses not found'}, status=status.HTTP_400_BAD_REQUEST)

        # total_price = sum([crs.price for crs in courses])

        order = Order.objects.create(device=device, student_name=request.data['student_name'], address=request.data['address'], whatsapp_number=request.data['whatsapp_number'], total_price=request.data.get('totalPrice', 0))
        # order.courses.set(courses)
        order.stored_ids = courses.replace("'", '"')
        order.save()
        order_data = {
            'student_name': order.student_name,
            'address': order.address,
            'whatsapp_number': order.whatsapp_number,
            'total_price': order.total_price,
            'courses': json.loads(order.stored_ids),
            'ordered_at': order.ordered_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        return Response(order_data, status=status.HTTP_201_CREATED)

class SubjectsAPIView(APIView):
    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrdersView(APIView):
    def get(self, request):
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        device_id = request.GET.get("device_id")

        if not from_date or not to_date or not device_id:
            return Response({"error": "device_id, from_date and to_date are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        orders = Order.objects.filter(ordered_at__date__range=[from_date, to_date], device__android_id=device_id)
        serializer = OrderSerializer(orders, many=True)

        return Response({"orders": serializer.data}, status=200)