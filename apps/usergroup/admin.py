from django.contrib import admin

from .models import UserGroup, GroupMember


class UserGroupInline(admin.TabularInline):
    model = GroupMember


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    inlines = [UserGroupInline]
