from django.contrib import admin
from django.db import models
from rangefilter.filters import DateRangeFilter
from django.db.models import Sum
from django.contrib.admin.views.main import ChangeList



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
    stored_ids = models.TextField(default="[]")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    student_name = models.CharField(max_length=255)
    address = models.TextField()
    whatsapp_number = models.CharField(max_length=15)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.address} - {self.device.android_id}"


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('android_id', 'registered_at')
    search_fields = ('android_id',)
    list_filter = ('registered_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'device', 'ordered_at')
    list_filter = ('device__android_id', 'whatsapp_number', ('ordered_at', DateRangeFilter))

    def changelist_view(self, request, extra_context=None):
        cl = ChangeList(
            request, self.model, self.list_display, self.list_display_links,
            self.list_filter, self.date_hierarchy, self.search_fields,
            self.list_select_related, self.list_per_page, self.list_max_show_all,
            self.list_editable, self, request.GET, self.get_queryset(request)
        )
        queryset = cl.get_queryset(request)  # Apply the filters

        # Aggregate sum of total_price for filtered entries
        total_price = queryset.aggregate(Sum('total_price'))['total_price__sum'] or 0.0

        request.session.total_price = total_price
        return super().changelist_view(request, extra_context=extra_context)

admin.site.site_title = "Iraq Academy"
admin.site.site_header = "Iraq Academy"
admin.site.index_title = "Iraq Academy Admin Panel"
