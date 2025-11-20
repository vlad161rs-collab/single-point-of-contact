from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.db import IntegrityError
from .models import UserProfile, UserRegistrationRequest, Department
from .forms import (
    UserRegistrationRequestForm, 
    UserProfileForm, 
    PasswordChangeCustomForm
)
from knowledgebase.models import Request, Article, Comment


def portal_home(request):
    """Главная страница портала самообслуживания"""
    return render(request, 'portal/home.html', {
        'user': request.user,
        'has_profile': hasattr(request.user, 'profile') if request.user.is_authenticated else False
    })


@login_required
def dashboard(request):
    """Личный кабинет в зависимости от роли"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    context = {
        'profile': profile,
        'user': request.user,
    }
    
    # Статистика для пользователя
    if profile.role == 'user':
        context['my_requests'] = Request.objects.filter(
            created_by=request.user
        )[:5]
        context['my_requests_count'] = Request.objects.filter(created_by=request.user).count()
        context['my_comments'] = Comment.objects.filter(user=request.user)[:5]
        return render(request, 'portal/dashboard_user.html', context)
    
    # Статистика для модератора
    elif profile.role == 'moderator':
        context['pending_requests'] = Request.objects.filter(status='New')[:10]
        context['pending_registrations'] = UserRegistrationRequest.objects.filter(status='pending')[:5]
        context['total_requests'] = Request.objects.count()
        context['total_articles'] = Article.objects.count()
        return render(request, 'portal/dashboard_moderator.html', context)
    
    # Статистика для администратора
    elif profile.role == 'admin' or request.user.is_superuser:
        context['pending_registrations'] = UserRegistrationRequest.objects.filter(status='pending')
        context['total_users'] = User.objects.count()
        context['total_requests'] = Request.objects.count()
        context['total_articles'] = Article.objects.count()
        context['requests_by_status'] = Request.objects.values('status').annotate(count=Count('id'))
        context['users_by_role'] = UserProfile.objects.values('role').annotate(count=Count('id'))
        return render(request, 'portal/dashboard_admin.html', context)
    
    # Статистика для службы поддержки
    elif profile.role == 'support':
        context['active_requests'] = Request.objects.filter(
            Q(status='New') | Q(status='In Progress')
        )[:10]
        context['my_assigned_requests'] = Request.objects.filter(
            status__in=['New', 'In Progress']
        )[:10]
        return render(request, 'portal/dashboard_support.html', context)
    
    # По умолчанию - обычный пользователь
    return render(request, 'portal/dashboard_user.html', context)


def register_request(request):
    """Запрос на регистрацию (требует одобрения админа)"""
    if request.user.is_authenticated:
        messages.info(request, 'Вы уже зарегистрированы.')
        return redirect('portal:home')

    if request.method == 'POST':
        form = UserRegistrationRequestForm(request.POST)
        if form.is_valid():
            reg_request = form.save()
            messages.success(
                request, 
                'Ваш запрос на регистрацию отправлен на рассмотрение администратору. '
                'Вы получите уведомление по email после рассмотрения.'
            )
            
            try:
                admin_email = getattr(settings, 'ADMIN_EMAIL', None)
                if admin_email:
                    send_mail(
                        subject=f'Новый запрос на регистрацию: {reg_request.username}',
                        message=f'Пользователь {reg_request.username} ({reg_request.email}) '
                               f'подал запрос на регистрацию. Роль: {reg_request.get_requested_role_display()}. '
                               f'Проверьте в админ-панели.',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[admin_email],
                        fail_silently=True,
                    )
            except Exception:
                pass
            
            return redirect('portal:register_success')
    else:
        form = UserRegistrationRequestForm()

    return render(request, 'portal/register.html', {'form': form})


def register_success(request):
    """Страница успешной отправки запроса на регистрацию"""
    return render(request, 'portal/register_success.html')


@login_required
def profile_view(request):
    """Просмотр и редактирование профиля пользователя"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('portal:profile')
        else:
            messages.error(request, 'Ошибка при сохранении формы. Проверьте введенные данные.')
    else:
        form = UserProfileForm(instance=profile, user=request.user)

    return render(request, 'portal/profile.html', {
        'form': form,
        'profile': profile,
    })


@login_required
def change_password(request):
    """Смена пароля пользователя"""
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен.')
            
            try:
                if request.user.email:
                    email_sent = send_mail(
                        subject='Пароль изменен',
                        message=f'Ваш пароль был успешно изменен.\n\n'
                               f'Если это были не вы, немедленно свяжитесь с администратором.\n\n'
                               f'Ссылка для входа: http://127.0.0.1:8000/accounts/login/',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[request.user.email],
                        fail_silently=False,
                    )
                    if not email_sent:
                        messages.warning(request, 'Пароль изменен, но не удалось отправить email-уведомление.')
            except Exception as e:
                import traceback
                print(f"Ошибка отправки email при смене пароля: {traceback.format_exc()}")
                messages.warning(request, f'Пароль изменен, но не удалось отправить email-уведомление: {str(e)}')
            
            return redirect('portal:profile')
    else:
        form = PasswordChangeCustomForm(request.user)

    return render(request, 'portal/change_password.html', {'form': form})


@login_required
@permission_required('portal.approve_userregistrationrequest', raise_exception=True)
def registration_requests_list(request):
    """Список запросов на регистрацию (для админов)"""
    status_filter = request.GET.get('status', '')
    requests = UserRegistrationRequest.objects.all().order_by('-created_at')
    
    if status_filter:
        requests = requests.filter(status=status_filter)
    
    pending_count = UserRegistrationRequest.objects.filter(status='pending').count()
    
    return render(request, 'portal/registration_requests.html', {
        'requests': requests,
        'pending_count': pending_count,
        'status_filter': status_filter,
    })


@login_required
@permission_required('portal.approve_userregistrationrequest', raise_exception=True)
def approve_registration(request, request_id):
    """Одобрение запроса на регистрацию"""
    reg_request = get_object_or_404(UserRegistrationRequest, id=request_id, status='pending')
    
    if request.method == 'POST':
        if User.objects.filter(username=reg_request.username).exists():
            reg_request.status = 'rejected'
            reg_request.reviewed_by = request.user
            reg_request.reviewed_at = timezone.now()
            reg_request.rejection_reason = f'Пользователь с именем "{reg_request.username}" уже существует в системе.'
            reg_request.save()
            messages.warning(
                request, 
                f'Заявка автоматически отклонена: пользователь с именем "{reg_request.username}" уже существует.'
            )
            return redirect('portal:registration_requests')
        
        if User.objects.filter(email=reg_request.email).exists():
            reg_request.status = 'rejected'
            reg_request.reviewed_by = request.user
            reg_request.reviewed_at = timezone.now()
            reg_request.rejection_reason = f'Пользователь с email "{reg_request.email}" уже существует в системе.'
            reg_request.save()
            messages.warning(
                request, 
                f'Заявка автоматически отклонена: пользователь с email "{reg_request.email}" уже существует.'
            )
            return redirect('portal:registration_requests')
        
        user_password = None
        try:
            is_staff = reg_request.requested_role in ['admin', 'moderator']
            user_password = reg_request.password_hash if reg_request.password_hash else None
            
            user = User.objects.create_user(
                username=reg_request.username,
                email=reg_request.email,
                first_name=reg_request.first_name,
                last_name=reg_request.last_name,
                is_active=True,
                is_staff=is_staff
            )
            
            if user_password:
                user.set_password(user_password)
            else:
                import secrets
                user_password = secrets.token_urlsafe(12)
                user.set_password(user_password)
            
            user.save()
        except IntegrityError as e:
            reg_request.status = 'rejected'
            reg_request.reviewed_by = request.user
            reg_request.reviewed_at = timezone.now()
            reg_request.rejection_reason = 'Ошибка при создании пользователя: пользователь с таким именем или email уже существует.'
            reg_request.save()
            messages.error(
                request, 
                'Заявка автоматически отклонена: пользователь с таким именем или email уже существует.'
            )
            return redirect('portal:registration_requests')
        
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.role = reg_request.requested_role
        profile.department = reg_request.department
        profile.phone = reg_request.phone
        profile.position = reg_request.position
        profile.save()
        
        reg_request.status = 'approved'
        reg_request.reviewed_by = request.user
        reg_request.reviewed_at = timezone.now()
        reg_request.save()
        
        try:
            if user.email:
                if user_password and user_password == reg_request.password_hash:
                    password_message = 'пароль, указанный при регистрации'
                else:
                    password_message = user_password
                
                email_sent = send_mail(
                    subject='Ваш запрос на регистрацию одобрен',
                    message=f'Ваш запрос на регистрацию одобрен администратором.\n\n'
                           f'Ваш логин: {user.username}\n'
                           f'Пароль: {password_message}\n\n'
                           f'Пожалуйста, войдите в систему по ссылке ниже.\n\n'
                           f'Ссылка для входа: http://127.0.0.1:8000/accounts/login/\n\n'
                           f'После входа вы сможете изменить пароль в личном кабинете.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                if email_sent:
                    messages.success(request, f'Запрос одобрен. Пользователь {user.username} создан. Email с данными для входа отправлен на {user.email}.')
                else:
                    messages.warning(request, f'Запрос одобрен. Пользователь {user.username} создан, но не удалось отправить email на {user.email}. Проверьте настройки email.')
        except Exception as e:
            import traceback
            error_msg = str(e)
            print(f"Ошибка отправки email: {traceback.format_exc()}")
            messages.warning(request, f'Запрос одобрен. Пользователь {user.username} создан, но не удалось отправить email: {error_msg}.')
        return redirect('portal:registration_requests')
    
    return render(request, 'portal/approve_registration.html', {
        'reg_request': reg_request
    })


@login_required
@permission_required('portal.approve_userregistrationrequest', raise_exception=True)
def reject_registration(request, request_id):
    """Отклонение запроса на регистрацию"""
    reg_request = get_object_or_404(UserRegistrationRequest, id=request_id, status='pending')
    
    if request.method == 'POST':
        rejection_reason = request.POST.get('rejection_reason', '')
        reg_request.status = 'rejected'
        reg_request.reviewed_by = request.user
        reg_request.reviewed_at = timezone.now()
        reg_request.rejection_reason = rejection_reason
        reg_request.save()
        
        try:
            if reg_request.email:
                send_mail(
                    subject='Ваш запрос на регистрацию отклонен',
                    message=f'К сожалению, ваш запрос на регистрацию был отклонен администратором.\n\n'
                           f'Причина: {rejection_reason or "Не указана"}\n\n'
                           f'Если у вас есть вопросы, свяжитесь с администратором.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[reg_request.email],
                    fail_silently=True,
                )
        except Exception:
            pass
        
        messages.success(request, 'Запрос отклонен.')
        return redirect('portal:registration_requests')
    
    return render(request, 'portal/reject_registration.html', {
        'reg_request': reg_request
    })


def kb_list(request):
    """Список статей базы знаний"""
    from urllib.parse import quote
    from django.urls import reverse
    q = request.GET.get('q', '')
    base = reverse('knowledgebase:index')
    return redirect(f"{base}?query={quote(q)}") if q else redirect(base)


def request_new(request):
    """Создание новой заявки"""
    return redirect('knowledgebase:requests-page')
