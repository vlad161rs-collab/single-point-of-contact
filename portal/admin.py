from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Department, UserRegistrationRequest


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'position', 'phone', 'created_at')
    list_filter = ('role', 'department', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'position')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Пользователь', {
            'fields': ('user', 'role')
        }),
        ('Информация', {
            'fields': ('department', 'position', 'phone')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserRegistrationRequest)
class UserRegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'requested_role', 'department', 'status', 'created_at', 'reviewed_by')
    list_filter = ('status', 'requested_role', 'department', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('created_at', 'reviewed_at')
    fieldsets = (
        ('Информация о пользователе', {
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone', 
                      'department', 'position', 'requested_role')
        }),
        ('Статус', {
            'fields': ('status', 'reviewed_by', 'reviewed_at', 'rejection_reason')
        }),
        ('Даты', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    actions = ['approve_registrations', 'reject_registrations']

    def approve_registrations(self, request, queryset):
        from django.contrib.auth.models import User
        from django.utils import timezone
        
        for reg_request in queryset.filter(status='pending'):
            user = User.objects.create_user(
                username=reg_request.username,
                email=reg_request.email,
                first_name=reg_request.first_name,
                last_name=reg_request.last_name,
                is_active=True
            )
            
            UserProfile.objects.create(
                user=user,
                role=reg_request.requested_role,
                department=reg_request.department,
                phone=reg_request.phone,
                position=reg_request.position
            )
            
            reg_request.status = 'approved'
            reg_request.reviewed_by = request.user
            reg_request.reviewed_at = timezone.now()
            reg_request.save()
            
        
        self.message_user(request, f"Одобрено запросов: {queryset.filter(status='pending').count()}")
    approve_registrations.short_description = "Одобрить выбранные запросы"

    def reject_registrations(self, request, queryset):
        from django.utils import timezone
        queryset.filter(status='pending').update(
            status='rejected',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f"Отклонено запросов: {queryset.filter(status='pending').count()}")
    reject_registrations.short_description = "Отклонить выбранные запросы"
