from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView
from django.db.models import Count, Sum
from .models import FileCategory, File, Purchase
# Create your views here.

class HomeView(View):
    template_name = 'core/index.html'
    def get(self, request):
        # دسته‌بندی‌ها با تعداد فایل‌ها
        categories = FileCategory.objects.all()
        for category in categories:
            category.file_count = category.file_set.filter(is_active=True).count()
        
        # آمار کلی
        total_files = File.objects.filter(is_active=True).count()
        total_downloads = File.objects.filter(is_active=True).aggregate(
            total=Sum('download_count')
        )['total'] or 0
        total_views = File.objects.filter(is_active=True).aggregate(
            total=Sum('view_count')
        )['total'] or 0
        
        # فایل‌های اخیر
        recent_files = File.objects.filter(is_active=True).order_by('-created_at')[:6]
        
        # فایل‌های محبوب
        popular_files = File.objects.filter(is_active=True).order_by('-download_count')[:6]

        context = {
            "categories": categories,
            "total_files": total_files,
            "total_downloads": total_downloads,
            "total_views": total_views,
            "recent_files": recent_files,
            "popular_files": popular_files,
        }
        return render(request, self.template_name, context)

class CategoryDetailView(DetailView):
    model = FileCategory
    template_name = 'core/category_detail.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = File.objects.filter(
            category=self.object,
            is_active=True
        ).order_by('-created_at')
        return context

class FileListView(ListView):
    model = File
    template_name = 'core/file_list.html'
    context_object_name = 'files'
    paginate_by = 12
    
    def get_queryset(self):
        return File.objects.filter(is_active=True).order_by('-created_at')

class FileDetailView(DetailView):
    model = File
    template_name = 'core/file_detail.html'
    context_object_name = 'file'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.increment_view()
        return obj