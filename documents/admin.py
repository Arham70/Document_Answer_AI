from django.contrib import admin
from .models import Document, UserProfile

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'uploaded_at', 'word_count']
    list_filter = ['status', 'uploaded_at']
    search_fields = ['title', 'user__username']
    readonly_fields = ['id', 'uploaded_at', 'processed_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']