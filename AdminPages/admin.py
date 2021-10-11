from django.contrib import admin
from Models.models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UsersAdmin(UserAdmin):
    list_display = ['email', 'username', 'ip_address', 'date_created', 'last_login', 'is_admin', 'is_staff', 'is_superuser']
    search_fields = ['email', 'username']
    readonly_fields = ['ip_address', 'verif_password', 'date_created', 'last_login']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class PostingAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    search_fields = ['title', 'desc', 'description']
    readonly_fields = ['author', 'created_at', 'updated_at']
    show_full_result_count = True
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class CommentAdmin(admin.ModelAdmin):
    list_display = ['username', 'created_at', 'updated_at']
    search_fields = ['username', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    show_full_result_count = True
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

#######################################################################################################
admin.site.register(User, UsersAdmin)
admin.site.register(PostingModels, PostingAdmin)
admin.site.register(CommentModels, CommentAdmin)