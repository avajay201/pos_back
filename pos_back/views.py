from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from .models import Order, Device
from datetime import datetime
import json
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['stored_ids'] = json.loads(instance.stored_ids)
        return representation


class RegisterOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        courses = str(request.data.get('courses'))
        if not courses:
            return Response({'error': 'Courses are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            device = Device.objects.get(device_id=request.data['device'], merchant=request.user)
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(device=device, merchant=request.user, student_name=request.data['student_name'], address=request.data['address'], whatsapp_number=request.data['whatsapp_number'], total_price=request.data.get('totalPrice', 0))
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


class OrdersView(APIView):
    permission_classes = [IsAuthenticated]

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

        orders = Order.objects.filter(ordered_at__date__range=[from_date, to_date], device__device_id=device_id, merchant=request.user)
        serializer = OrderSerializer(orders, many=True)

        return Response({"orders": serializer.data}, status=200)


class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        device_id = request.data.get('device_id')
        
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)

        if user is None:
            user = User.objects.create_user(username=username, password=password)

        refresh = RefreshToken.for_user(user)

        Device.objects.get_or_create(device_id=device_id, merchant=user)

        return Response({
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
