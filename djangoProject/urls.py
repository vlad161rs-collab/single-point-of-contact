from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import redirect

def redirect_to_login(request):
    # При первом заходе — сразу на страницу входа
    return redirect('login')

urlpatterns = [
    # --- Корень сайта ведёт на login ---
    path('', redirect_to_login, name='root'),

    path('admin/', admin.site.urls),

    # Портал самообслуживания
    path('portal/', include(('portal.urls', 'portal'), namespace='portal')),

    # База знаний (Единая точка обращений)
    path('knowledgebase/', include(('knowledgebase.urls', 'knowledgebase'), namespace='knowledgebase')),

    # --- Аутентификация ---
    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='knowledgebase/login.html'),
         name='login'),

    path('accounts/logout/',
         auth_views.LogoutView.as_view(next_page='login'),
         name='logout'),

    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

# Раздача статических и медиа файлов
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    from django.views.static import serve
    from django.urls import re_path
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]


