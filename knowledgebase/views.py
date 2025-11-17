from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Article, Request, Comment
from .forms import ArticleForm, RequestForm, CommentForm
from .serializers import RequestSerializer
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.http import require_POST
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib import messages


def index(request):
    articles = Article.objects.all()
    query = request.GET.get('query')
    sort_by = request.GET.get('sort_by')

    if query:
        articles = articles.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    if sort_by:
        articles = articles.order_by(sort_by)

    return render(request, 'knowledgebase/index.html', {'articles': articles})


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    comments = article.comments.select_related('user').all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponseForbidden('Только для авторизованных пользователей')

        form = CommentForm(request.POST)
        if form.is_valid():
            try:
                comment = form.save(commit=False)
                comment.article = article
                comment.request = None
                if request.user and request.user.is_authenticated:
                    comment.user = request.user
                else:
                    messages.error(request, 'Вы должны быть авторизованы для добавления комментария.')
                    return redirect('knowledgebase:article_detail', article_id=article.id)
                comment.full_clean()
                comment.save()
                messages.success(request, 'Комментарий успешно добавлен.')
                return redirect('knowledgebase:article_detail', article_id=article.id)
            except Exception as e:
                import traceback
                messages.error(request, f'Ошибка при сохранении комментария: {str(e)}')
                print(f"Ошибка сохранения комментария: {traceback.format_exc()}")
        else:
            messages.error(request, f'Пожалуйста, исправьте ошибки в форме: {form.errors}')
    else:
        form = CommentForm()

    return render(request, 'knowledgebase/detail.html', {
        'article': article,
        'comments': comments,
        'form': form,
    })


@login_required
@permission_required('knowledgebase.add_article', raise_exception=True)
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Статья успешно создана.')
            return redirect('knowledgebase:index')
    else:
        form = ArticleForm()
    return render(request, 'knowledgebase/article_form.html', {'form': form})


@login_required
def requests_page_view(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.created_by = request.user
            from .utils import auto_classify_request
            if not request_obj.category or request_obj.category == 'Uncategorized':
                request_obj.category = auto_classify_request(
                    request_obj.title, 
                    request_obj.description
                )
            request_obj.save()
            messages.success(request, 'Заявка успешно создана.')
            return redirect('knowledgebase:requests-page')
    else:
        form = RequestForm()

    query = request.GET.get('query', '')
    status_filter = request.GET.get('status', '')
    
    requests = Request.objects.all()
    
    if query:
        requests = requests.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    
    if status_filter:
        requests = requests.filter(status=status_filter)
    
    try:
        requests = requests.order_by('-created_at')
    except:
        requests = requests.order_by('-id')
    
    return render(
        request,
        'knowledgebase/requests_page.html',
        {
            'form': form, 
            'requests': requests,
            'query': query,
            'status_filter': status_filter,
        },
    )


@login_required
def optimized_requests_view(request):
    # Optimize query by prefetching related comments
    requests = Request.objects.prefetch_related('comments__user').all()
    return render(request, 'knowledgebase/requests.html', {'requests': requests})


@require_POST
@permission_required('knowledgebase.change_request', raise_exception=True)
@login_required
def change_request_status(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    old_status = req.status
    new_status = request.POST.get('status')
    
    # Проверяем, что статус валидный
    valid_statuses = ['New', 'In Progress', 'Completed', 'Cancelled']
    if new_status in valid_statuses:
        req.status = new_status
        req.save()
        
        from .signals import send_request_status_notification
        user_email = req.created_by.email if req.created_by and req.created_by.email else None
        send_request_status_notification(req, old_status, req.status, user_email=user_email)
        
        status_display = req.get_status_display()
        messages.success(request, f'Статус заявки изменен на "{status_display}".')
    else:
        messages.error(request, 'Неверный статус.')
    
    return redirect('knowledgebase:requests-page')


@login_required
@permission_required('knowledgebase.delete_request', raise_exception=True)
@require_POST
def delete_request(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    req.delete()
    messages.success(request, 'Заявка успешно удалена.')
    return redirect('knowledgebase:requests-page')


@login_required
@require_POST
def add_comment_to_request(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        try:
            comment = form.save(commit=False)
            comment.request = req
            comment.article = None
            if request.user and request.user.is_authenticated:
                comment.user = request.user
            else:
                messages.error(request, 'Вы должны быть авторизованы для добавления комментария.')
                return redirect('knowledgebase:requests-page')
            comment.full_clean()
            comment.save()
            messages.success(request, 'Комментарий успешно добавлен.')
        except Exception as e:
            import traceback
            messages.error(request, f'Ошибка при сохранении комментария: {str(e)}')
            print(f"Ошибка сохранения комментария: {traceback.format_exc()}")
    else:
        messages.error(request, f'Пожалуйста, исправьте ошибки в форме: {form.errors}')

    return redirect('knowledgebase:requests-page')


class RequestAPI(APIView):
    """
    API для работы с заявками.
    - GET: доступен всем (в т.ч. анонимным)
    - POST: только авторизованным пользователям
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        requests_qs = Request.objects.all()
        serializer = RequestSerializer(requests_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
def request_detail(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    comments = req.comments.select_related('user').all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponseForbidden('Только для авторизованных пользователей')
            
        form = CommentForm(request.POST)
        if form.is_valid():
            try:
                comment = form.save(commit=False)
                comment.request = req
                comment.article = None
                if request.user and request.user.is_authenticated:
                    comment.user = request.user
                else:
                    messages.error(request, 'Вы должны быть авторизованы для добавления комментария.')
                    return redirect('knowledgebase:request_detail', request_id=req.id)
                comment.full_clean()
                comment.save()
                messages.success(request, 'Комментарий успешно добавлен.')
                return redirect('knowledgebase:request_detail', request_id=req.id)
            except Exception as e:
                import traceback
                messages.error(request, f'Ошибка при сохранении комментария: {str(e)}')
                print(f"Ошибка сохранения комментария: {traceback.format_exc()}")
        else:
            messages.error(request, f'Пожалуйста, исправьте ошибки в форме: {form.errors}')
    else:
        form = CommentForm()

    return render(request, 'knowledgebase/request_detail.html', {
        'req': req,
        'comments': comments,
        'form': form,
    })


@login_required
@permission_required('knowledgebase.change_article', raise_exception=True)
def article_edit(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            if not article.author:
                article.author = request.user
            article.save()
            messages.success(request, 'Статья успешно обновлена.')
            return redirect('knowledgebase:article_detail', article_id=article.id)
    else:
        form = ArticleForm(instance=article)

    return render(
        request,
        'knowledgebase/article_form.html',
        {'form': form, 'article': article},
    )


@login_required
@require_POST
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    author_id = getattr(comment, 'user_id', None)

    if not (
        (author_id is not None and author_id == request.user.id)
        or request.user.has_perm('knowledgebase.delete_comment')
    ):
        return HttpResponseForbidden('Недостаточно прав')

    parent_article = getattr(comment, 'article', None)
    parent_request = getattr(comment, 'request', None)

    comment.delete()
    messages.success(request, 'Комментарий успешно удален.')

    if parent_article:
        return redirect('knowledgebase:article_detail', article_id=parent_article.id)
    if parent_request:
        return redirect('knowledgebase:request_detail', request_id=parent_request.id)

    return HttpResponseBadRequest(
        "Comment is not associated with an article or request."
    )


@login_required
@permission_required('knowledgebase.delete_article', raise_exception=True)
@require_POST
def article_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.delete()
    messages.success(request, "Статья успешно удалена.")
    return redirect('knowledgebase:index')


def home_view(request):
    return render(request, 'knowledgebase/home.html')
