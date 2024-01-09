"""
URL configuration for bookstore_firaas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.http import HttpResponse
# from django.http.response import JsonResponse
from django.shortcuts import render
from bookstore_firaas.modules.admin.views import AdminViews
from bookstore_firaas.modules.user.views import UserViews
from bookstore_firaas.modules.register.views import RegisterViews
from bookstore_firaas.modules.forgot_password.views import ForgotPasswordViews
from bookstore_firaas.modules.oauth.views import OauthViews
from bookstore_firaas.modules.me.views import MeViews
from bookstore_firaas.modules.product.views import ProductViews
# from bookstore_firaas.modules.order.views import OrderViews
# from bookstore_firaas.modules.class_room.views import ClassRoomViews
# from bookstore_firaas.modules.webhook.views import WebhookViews
# from bookstore_firaas.modules.dashboard.views import DashboardViews

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/admins', AdminViews.as_view()),
    path('api/v1/admins/<int:id>/', AdminViews.as_view()),
    path('api/v1/users', UserViews.as_view()),
    path('api/v1/users/<int:id>/', UserViews.as_view()),
    path('api/v1/registers', RegisterViews.as_view()),
    path('api/v1/forgot_passwords', ForgotPasswordViews.as_view()),
    path('api/v1/oauth', OauthViews.as_view()),
    path('api/v1/me', MeViews.as_view()),
    path('api/v1/products', ProductViews.as_view()),
    path('api/v1/products/<int:id>/', ProductViews.as_view()),
    # path('api/v1/orders', OrderViews.as_view()),
    # path('api/v1/orders/<int:id>/', OrderViews.as_view()),
    # path('api/v1/class_rooms', ClassRoomViews.as_view()),
    # path('api/v1/class_rooms/<int:id>/', ClassRoomViews.as_view()),
    # path('api/v1/webhooks', WebhookViews.as_view()),
    # path('api/v1/dashboards', DashboardViews.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)