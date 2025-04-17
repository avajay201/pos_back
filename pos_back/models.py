from django.contrib import admin
from django.db import models
from rangefilter.filters import DateRangeFilter
from django.db.models import Sum
from django.contrib.admin.views.main import ChangeList
from decimal import Decimal
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    percentage = models.FloatField(default=0.0)
    can_generate_bulk_coupons = models.BooleanField(default=False)
    api_token = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.pk:
            old = CustomUser.objects.get(pk=self.pk)
            if old.password != self.password:
                self.set_password(self.password)
        else:
            self.set_password(self.password)

        super().save(*args, **kwargs)


class Order(models.Model):
    merchant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stored_ids = models.TextField(default="[]")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    student_name = models.CharField(max_length=255)
    address = models.TextField()
    whatsapp_number = models.CharField(max_length=15)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order from {self.merchant.username}"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'ordered_at')
    list_filter = ('whatsapp_number', 'merchant__username', ('ordered_at', DateRangeFilter))

    def changelist_view(self, request, extra_context=None):
        cl = ChangeList(
            request, self.model, self.list_display, self.list_display_links,
            self.list_filter, self.date_hierarchy, self.search_fields,
            self.list_select_related, self.list_per_page, self.list_max_show_all,
            self.list_editable, self, request.GET, self.get_queryset(request)
        )
        queryset = cl.get_queryset(request)

        merchant__username = request.GET.get('merchant__username')
        if merchant__username:
            queryset = queryset.filter(merchant__username=merchant__username)

        total_price = queryset.aggregate(Sum('total_price'))['total_price__sum'] or 0.0
        discount_price = total_price
        if merchant__username and queryset.count() > 0:
            merchant = CustomUser.objects.filter(username=merchant__username).first()
            if merchant:
                discount_price = total_price - (total_price * (Decimal(merchant.percentage) / Decimal(100)))

        request.session.total_price = total_price
        request.session.discount_price = discount_price
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(CustomUser)

admin.site.site_title = "Iraq Academy"
admin.site.site_header = "Iraq Academy"
admin.site.index_title = "Iraq Academy Admin Panel"
