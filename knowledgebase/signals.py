from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import Request, Comment


@receiver(post_save, sender=Request)
def notify_request_created_or_updated(sender, instance, created, **kwargs):
    """Уведомление о создании или изменении заявки"""
    if created:
        try:
            admin_email = getattr(settings, 'ADMIN_EMAIL', None)
            if admin_email:
                subject = f'Новая заявка: {instance.title}'
                message = f'Создана новая заявка:\n\n'
                message += f'Название: {instance.title}\n'
                message += f'Описание: {instance.description[:200]}...\n'
                message += f'Категория: {instance.get_category_display()}\n'
                message += f'Статус: {instance.get_status_display()}\n\n'
                request_path = reverse('knowledgebase:request_detail', args=[instance.id])
                request_url = f"{settings.BASE_URL}{request_path}"
                message += f'Просмотреть заявку: {request_url}'
                
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[admin_email],
                    fail_silently=True,
                )
        except Exception:
            pass
    else:
        pass


@receiver(post_save, sender=Comment)
def notify_comment_added(sender, instance, created, **kwargs):
    """Уведомление о добавлении комментария"""
    if created and instance.user:
        try:
            recipients = []
            
            if instance.request:
                if instance.request.created_by and instance.request.created_by.email:
                    if instance.request.created_by.email != instance.user.email:
                        recipients.append(instance.request.created_by.email)
                
                admin_email = getattr(settings, 'ADMIN_EMAIL', None)
                if admin_email and admin_email not in recipients:
                    recipients.append(admin_email)
            
            elif instance.article:
                if instance.article.author and instance.article.author.email:
                    if instance.article.author.email != instance.user.email:
                        recipients.append(instance.article.author.email)
                
                admin_email = getattr(settings, 'ADMIN_EMAIL', None)
                if admin_email and admin_email not in recipients:
                    recipients.append(admin_email)
            
            if recipients:
                subject = 'Новый комментарий'
                message = f'Пользователь {instance.user.get_full_name() or instance.user.username} добавил комментарий:\n\n'
                message += f'{instance.text[:200]}{"..." if len(instance.text) > 200 else ""}\n\n'
                
                if instance.request:
                    request_path = reverse('knowledgebase:request_detail', args=[instance.request.id])
                    request_url = f"{settings.BASE_URL}{request_path}"
                    message += f'К заявке: {instance.request.title}\n'
                    message += f'Ссылка: {request_url}'
                elif instance.article:
                    article_path = reverse('knowledgebase:article_detail', args=[instance.article.id])
                    article_url = f"{settings.BASE_URL}{article_path}"
                    message += f'К статье: {instance.article.title}\n'
                    message += f'Ссылка: {article_url}'
                
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=recipients,
                    fail_silently=True,
                )
        except Exception as e:
            import traceback
            print(f"Ошибка отправки email при добавлении комментария: {traceback.format_exc()}")


def send_request_status_notification(request_obj, old_status, new_status, user_email=None):
    """Отправка уведомления об изменении статуса заявки"""
    try:
        recipients = []
        
        if user_email:
            recipients.append(user_email)
        
        if request_obj.created_by and request_obj.created_by.email:
            if request_obj.created_by.email not in recipients:
                recipients.append(request_obj.created_by.email)
        
        admin_email = getattr(settings, 'ADMIN_EMAIL', None)
        if admin_email and admin_email not in recipients:
            recipients.append(admin_email)
        
        if recipients:
            status_display_map = {
                'New': 'Новая',
                'In Progress': 'В работе',
                'Completed': 'Завершена',
                'Cancelled': 'Отменена',
            }
            old_status_display = status_display_map.get(old_status, old_status)
            new_status_display = status_display_map.get(new_status, new_status)
            
            subject = f'Изменен статус заявки: {request_obj.title}'
            message = f'Статус заявки изменен:\n\n'
            message += f'Заявка: {request_obj.title}\n'
            message += f'Описание: {request_obj.description[:200]}{"..." if len(request_obj.description) > 200 else ""}\n\n'
            message += f'Старый статус: {old_status_display}\n'
            message += f'Новый статус: {new_status_display}\n\n'
            request_path = reverse('knowledgebase:request_detail', args=[request_obj.id])
            request_url = f"{settings.BASE_URL}{request_path}"
            message += f'Просмотреть заявку: {request_url}'
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                fail_silently=True,
            )
    except Exception as e:
        import traceback
        print(f"Ошибка отправки email при изменении статуса заявки: {traceback.format_exc()}")

