from django.contrib import admin
from django.db import models
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import datetime



class Subject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=255)
    description = models.TextField()
    profile_pic = models.ImageField(upload_to='courses/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Device(models.Model):
    android_id = models.CharField(max_length=255, unique=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.android_id

class Order(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    # courses = models.ManyToManyField(Course)
    stored_ids = models.TextField(default="[]")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    student_name = models.CharField(max_length=255)
    address = models.TextField()
    whatsapp_number = models.CharField(max_length=15)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.address} - {self.device.android_id}"


from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import datetime


class CustomDateRangeFilter(SimpleListFilter):
    title = _('Order Date Range')  # Title in admin panel
    parameter_name = 'ordered_at'  # Query parameter

    def lookups(self, request, model_admin):
        """Not used, but required for SimpleListFilter"""
        return ()

    def queryset(self, request, queryset):
        """Filter the queryset based on user input."""
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        if from_date:
            queryset = queryset.filter(ordered_at__gte=from_date)
        if to_date:
            queryset = queryset.filter(ordered_at__lte=to_date)

        return queryset

# admin.site.register(Subject)
# admin.site.register(Teacher)
# admin.site.register(Course)
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('android_id', 'registered_at')
    search_fields = ('android_id',)
    list_filter = ('registered_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'device', 'total_price', 'ordered_at')
    search_fields = ('student_name', 'device__android_id', 'whatsapp_number', 'address')
    list_filter = ('total_price', 'device__android_id', 'whatsapp_number', 'ordered_at')


admin.site.site_title = "Iraq Academy"
admin.site.site_header = "Iraq Academy"
admin.site.index_title = "Iraq Academy Admin Panel"
