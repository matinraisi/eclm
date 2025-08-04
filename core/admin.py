from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import File, FileCategory, Purchase

@admin.register(FileCategory)
class FileCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview', 'file_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 5px;" />',
                obj.image.url
            )
        return "بدون تصویر"
    image_preview.short_description = 'تصویر'
    
    def file_count(self, obj):
        return obj.file_set.filter(is_active=True).count()
    file_count.short_description = 'تعداد فایل‌ها'

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'file_type', 'file_size', 'download_count', 'view_count', 'is_active', 'created_at']
    list_filter = ['file_type', 'category', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['price', 'is_active']
    readonly_fields = ['download_count', 'view_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'description', 'file', 'file_type', 'category')
        }),
        ('قیمت و وضعیت', {
            'fields': ('price', 'is_active')
        }),
        ('آمار', {
            'fields': ('download_count', 'view_count'),
            'classes': ('collapse',)
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def file_size(self, obj):
        return obj.get_file_size()
    file_size.short_description = 'اندازه فایل'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')
    
    actions = ['activate_files', 'deactivate_files', 'reset_stats']
    
    def activate_files(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} فایل فعال شد.')
    activate_files.short_description = 'فعال کردن فایل‌های انتخاب شده'
    
    def deactivate_files(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} فایل غیرفعال شد.')
    deactivate_files.short_description = 'غیرفعال کردن فایل‌های انتخاب شده'
    
    def reset_stats(self, request, queryset):
        updated = queryset.update(download_count=0, view_count=0)
        self.message_user(request, f'آمار {updated} فایل ریست شد.')
    reset_stats.short_description = 'ریست کردن آمار فایل‌های انتخاب شده'

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'file', 'amount', 'status', 'purchased_at']
    list_filter = ['status', 'purchased_at', 'user']
    search_fields = ['user__username', 'file__title', 'transaction_id']
    readonly_fields = ['purchased_at']
    
    fieldsets = (
        ('اطلاعات خرید', {
            'fields': ('user', 'file', 'amount', 'status')
        }),
        ('اطلاعات تراکنش', {
            'fields': ('transaction_id', 'purchased_at')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'file')
    
    actions = ['mark_completed', 'mark_failed', 'mark_cancelled']
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} خرید تکمیل شد.')
    mark_completed.short_description = 'علامت‌گذاری به عنوان تکمیل شده'
    
    def mark_failed(self, request, queryset):
        updated = queryset.update(status='failed')
        self.message_user(request, f'{updated} خرید ناموفق شد.')
    mark_failed.short_description = 'علامت‌گذاری به عنوان ناموفق'
    
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} خرید لغو شد.')
    mark_cancelled.short_description = 'علامت‌گذاری به عنوان لغو شده'
