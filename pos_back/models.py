from django.contrib import admin
from django.db import models
from rangefilter.filters import DateRangeFilter
from django.db.models import Sum
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.models import User


# class Device(models.Model):
#     device_id = models.CharField(max_length=255, unique=True)
#     merchant = models.ForeignKey(User, on_delete=models.CASCADE)
#     registered_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.device_id

class Order(models.Model):
    # device = models.ForeignKey(Device, on_delete=models.CASCADE)
    merchant = models.ForeignKey(User, on_delete=models.CASCADE)
    stored_ids = models.TextField(default="[]")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    student_name = models.CharField(max_length=255)
    address = models.TextField()
    whatsapp_number = models.CharField(max_length=15)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order from {self.merchant.username}"


# @admin.register(Device)
# class DeviceAdmin(admin.ModelAdmin):
#     list_display = ('device_id', 'registered_at')
#     search_fields = ('device_id',)
#     list_filter = ('registered_at', 'merchant')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'ordered_at')
    list_filter = ('whatsapp_number', 'merchant', ('ordered_at', DateRangeFilter))

    def changelist_view(self, request, extra_context=None):
        cl = ChangeList(
            request, self.model, self.list_display, self.list_display_links,
            self.list_filter, self.date_hierarchy, self.search_fields,
            self.list_select_related, self.list_per_page, self.list_max_show_all,
            self.list_editable, self, request.GET, self.get_queryset(request)
        )
        queryset = cl.get_queryset(request)

        total_price = queryset.aggregate(Sum('total_price'))['total_price__sum'] or 0.0

        request.session.total_price = total_price
        return super().changelist_view(request, extra_context=extra_context)

admin.site.site_title = "Iraq Academy"
admin.site.site_header = "Iraq Academy"
admin.site.index_title = "Iraq Academy Admin Panel"
