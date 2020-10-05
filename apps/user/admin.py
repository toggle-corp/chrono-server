from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, User

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    fieldsets = (
        (None, {
            'fields': (
                'username', 'email',
                'first_name', 'last_name',
                'password',
                'last_login', 'date_joined',
                'is_staff', 'is_superuser',
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('last_login', 'date_joined', )
    search_fields = ('username', 'email', )
    list_display = (
        'username', 'email', 'first_name', 'last_name',
    )
    list_select_related = ('profile', )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)