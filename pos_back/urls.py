"""
URL configuration for pos_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (RegisterOrderAPIView, OrdersView, LoginAPI,
                    export_xlsx, TeacherAPIView, TeacherCourseSectionsAPIView,
                    GradesAPIView, GradeCourseSectionsAPIView, CourseCouponsAPIView,
                    CoursesAPIView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginAPI.as_view()),
    path('api/order/', RegisterOrderAPIView.as_view()),
    path('api/orders/', OrdersView.as_view()),
    path("export-xlsx/", export_xlsx, name="export_xlsx"),
    path('api/teachers/', TeacherAPIView.as_view()),
    path('api/teacher-course-sections/<int:teacher_id>/', TeacherCourseSectionsAPIView.as_view()),
    path('api/grades/', GradesAPIView.as_view()),
    path('api/grade-course-sections/', GradeCourseSectionsAPIView.as_view()),
    path('api/course-coupons/', CourseCouponsAPIView.as_view()),
    path('api/courses/<int:id>/', CoursesAPIView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
