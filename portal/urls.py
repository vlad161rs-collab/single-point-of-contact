from django.urls import path
from . import views

app_name = "portal"

urlpatterns = [
    path("", views.portal_home, name="home"),
    path("kb/", views.kb_list, name="kb_list"),
    path("request/new/", views.request_new, name="request_new"),
    # Портал самообслуживания
    path("register/", views.register_request, name="register"),
    path("register/success/", views.register_success, name="register_success"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/change-password/", views.change_password, name="change_password"),
    path("dashboard/", views.dashboard, name="dashboard"),
    # Админские функции
    path("admin/registrations/", views.registration_requests_list, name="registration_requests"),
    path("admin/registrations/<int:request_id>/approve/", views.approve_registration, name="approve_registration"),
    path("admin/registrations/<int:request_id>/reject/", views.reject_registration, name="reject_registration"),
]