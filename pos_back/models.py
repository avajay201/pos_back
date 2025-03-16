from django.contrib import admin
from django.db import models



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
    buyer = models.CharField(max_length=255)
    buyer_email = models.EmailField()
    buyer_phone = models.CharField(max_length=15)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.buyer_email} - {self.device.android_id}"


admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Device)
admin.site.register(Order)


admin.site.site_title = "Horizon Star"
admin.site.site_header = "Horizon Star"
admin.site.index_title = "Horizon Star Admin Panel"
