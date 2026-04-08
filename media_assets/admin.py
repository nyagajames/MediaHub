from django.contrib import admin
from .models import MediaAssets


# Register your models here.`
@admin.register(MediaAssets)
class MediaAssetsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_by', 'created_at', 'is_public')
    list_filter = ('category', 'is_public', 'created_at')
    search_fields = ('title', 'description', 'uploaded_by__username')
    readonly_fields = ('created_at', 'updated_at', 'view_count')
    date_hierarchy = 'created_at'