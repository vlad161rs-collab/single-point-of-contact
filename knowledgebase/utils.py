import re
from .models import Request


def auto_classify_request(title, description):
    text = f"{title} {description}".lower()
    
    technical_keywords = [
        'ошибка', 'не работает', 'сломалось', 'баг', 'bug', 'error',
        'технический', 'система', 'программа', 'приложение', 'сервер',
        'интернет', 'сеть', 'компьютер', 'принтер', 'сканер', 'оборудование'
    ]
    
    content_keywords = [
        'контент', 'статья', 'текст', 'изображение', 'фото', 'видео',
        'публикация', 'материал', 'информация', 'документ', 'файл',
        'редактирование', 'изменение', 'добавить', 'удалить'
    ]
    
    technical_score = sum(1 for keyword in technical_keywords if keyword in text)
    content_score = sum(1 for keyword in content_keywords if keyword in text)
    
    if technical_score > content_score and technical_score > 0:
        return 'Technical'
    elif content_score > technical_score and content_score > 0:
        return 'Content'
    else:
        return 'Uncategorized'


def auto_assign_request(request_obj):
    category = request_obj.category
    
    if category == 'Technical':
        return 'support'
    elif category == 'Content':
        return 'moderator'
    else:
        return 'admin'


def process_email_request(email_subject, email_body, sender_email):
    title = email_subject[:255]
    category = auto_classify_request(title, email_body)
    
    request_obj = Request.objects.create(
        title=title,
        description=email_body,
        category=category,
        status='New'
    )
    
    auto_assign_request(request_obj)
    
    return request_obj

