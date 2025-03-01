from django.contrib import admin

from cord4_task.custom_auth.models import ApplicationUser


# Register your models here.
class ApplicationUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username')


admin.site.register(ApplicationUser, ApplicationUserAdmin)

