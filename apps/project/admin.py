from django.contrib import admin

from .models import Client, Project, Tag


@admin.register(Client)
class RegisterAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
