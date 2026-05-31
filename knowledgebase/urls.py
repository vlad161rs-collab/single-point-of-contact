from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'knowledgebase'


def redirect_to_login(request):
    return redirect('login')


def redirect_to_logout(request):
    return redirect('logout')


urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home_view, name='home'),
    path('login/', redirect_to_login, name='login'),
    path('logout/', redirect_to_logout, name='logout'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('article/create/', views.article_create, name='article_create'),
    path('article/edit/<int:article_id>/', views.article_edit, name='article_edit'),
    path('article/delete/<int:article_id>/', views.article_delete, name='article_delete'),
    path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('requests-page/', views.requests_page_view, name='requests-page'),
    path('requests/', views.optimized_requests_view, name='requests'),
    path('requests/<int:request_id>/', views.request_detail, name='request_detail'),
    path('requests/<int:request_id>/change-status/', views.change_request_status, name='change-request-status'),
    path('requests/<int:request_id>/delete/', views.delete_request, name='delete-request'),
    path('requests/<int:request_id>/add-comment/', views.add_comment_to_request, name='add-comment'),
    path('api/requests/', views.RequestAPI.as_view(), name='request-api'),
]

