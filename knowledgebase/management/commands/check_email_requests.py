"""
Management команда для проверки почты и создания заявок
В продакшене можно настроить cron для автоматической проверки
"""
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from knowledgebase.utils import process_email_request
import imaplib
import email
from email.header import decode_header


class Command(BaseCommand):
    help = 'Проверяет почту и создает заявки из писем'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email адрес для проверки',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Пароль от email',
        )

    def handle(self, *args, **options):
        email_address = options.get('email') or 'requests@example.com'
        password = options.get('password')
        
        if not password:
            self.stdout.write(
                self.style.ERROR('Необходимо указать пароль для email')
            )
            return
        
        try:
            # Подключение к почтовому серверу (пример для Gmail)
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(email_address, password)
            mail.select("inbox")
            
            # Поиск непрочитанных писем
            status, messages = mail.search(None, "UNSEEN")
            email_ids = messages[0].split()
            
            processed_count = 0
            
            for email_id in email_ids:
                try:
                    # Получение письма
                    status, msg_data = mail.fetch(email_id, "(RFC822)")
                    email_body = msg_data[0][1]
                    email_message = email.message_from_bytes(email_body)
                    
                    subject = decode_header(email_message["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    
                    sender = email_message["From"]
                    
                    # Получение текста письма
                    body = ""
                    if email_message.is_multipart():
                        for part in email_message.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = email_message.get_payload(decode=True).decode()
                    
                    # Создание заявки
                    request_obj = process_email_request(subject, body, sender)
                    processed_count += 1
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Создана заявка #{request_obj.id}: {request_obj.title}'
                        )
                    )
                    
                    # Отправка подтверждения (опционально)
                    # reply = EmailMessage(
                    #     subject=f'Re: {subject}',
                    #     body='Ваша заявка получена и обрабатывается.',
                    #     to=[sender]
                    # )
                    # reply.send()
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Ошибка обработки письма: {e}')
                    )
            
            mail.close()
            mail.logout()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Обработано писем: {processed_count}'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка подключения к почте: {e}')
            )

