from django.db import models
from django.conf import settings
from django.utils import timezone
import os
import uuid

class FileCategory(models.Model):
    """دسته‌بندی فایل‌ها"""
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    image = models.ImageField(upload_to='category_images/', blank=True, verbose_name="تصویر دسته‌بندی")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "دسته‌بندی فایل"
        verbose_name_plural = "دسته‌بندی‌های فایل"
        ordering = ['name']
    
    def __str__(self):
        return self.name

def file_upload_path(instance, filename):
    """تعیین مسیر آپلود فایل"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    if instance.category:
        return f"files/{instance.category.name}/{filename}"
    return f"files/uncategorized/{filename}"

class File(models.Model):
    """مدل فایل برای فروش"""
    FILE_TYPES = [
        ('document', 'سند'),
        ('image', 'تصویر'),
        ('video', 'ویدیو'),
        ('audio', 'صوت'),
        ('archive', 'آرشیو'),
        ('code', 'کد'),
        ('other', 'سایر'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="عنوان")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    file = models.FileField(upload_to=file_upload_path, verbose_name="فایل")
    file_type = models.CharField(max_length=20, choices=FILE_TYPES, verbose_name="نوع فایل")
    category = models.ForeignKey(FileCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="دسته‌بندی")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت (تومان)")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    download_count = models.PositiveIntegerField(default=0, verbose_name="تعداد دانلود")
    view_count = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        verbose_name = "فایل"
        verbose_name_plural = "فایل‌ها"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_file_size(self):
        """دریافت اندازه فایل"""
        try:
            size = self.file.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        except:
            return "نامشخص"
    
    def get_file_extension(self):
        """دریافت پسوند فایل"""
        return os.path.splitext(self.file.name)[1].lower()
    
    def increment_download(self):
        """افزایش شمارنده دانلود"""
        self.download_count += 1
        self.save(update_fields=['download_count'])
    
    def increment_view(self):
        """افزایش شمارنده بازدید"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

class Purchase(models.Model):
    """مدل خرید فایل"""
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('completed', 'تکمیل شده'),
        ('failed', 'ناموفق'),
        ('cancelled', 'لغو شده'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="کاربر")
    file = models.ForeignKey(File, on_delete=models.CASCADE, verbose_name="فایل")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مبلغ پرداختی")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name="شناسه تراکنش")
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ خرید")
    
    class Meta:
        verbose_name = "خرید"
        verbose_name_plural = "خریدها"
        ordering = ['-purchased_at']
        unique_together = ['user', 'file']  # هر کاربر فقط یک بار می‌تواند فایل را بخرد
    
    def __str__(self):
        return f"{self.user.username} - {self.file.title}"
