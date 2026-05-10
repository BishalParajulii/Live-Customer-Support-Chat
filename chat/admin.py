from django.contrib import admin

from .models import ChatMessage, ChatSession


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer_name",)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "sender", "is_read", "timestamp")
    list_filter = ("sender", "is_read", "timestamp")
    search_fields = ("content", "session__customer_name")
