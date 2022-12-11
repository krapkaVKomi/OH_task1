from django.contrib import admin


from django.contrib import admin

from .models import Checks


class CheckAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key', 'check_type', 'point_id')


admin.site.register(Checks, CheckAdmin)
