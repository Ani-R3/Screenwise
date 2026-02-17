from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Video

# This is the line that was causing the error. We are removing it.
# admin.site.register(CustomUser) 

# We will keep the registration for the Video model here.
admin.site.register(Video)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Profile Info', {'fields': ('name', 'profile_pic', 'bio')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'is_staff', 'is_active')}
        ),
    )

# This is now the ONLY registration for CustomUser, which is correct.
admin.site.register(CustomUser, CustomUserAdmin)

