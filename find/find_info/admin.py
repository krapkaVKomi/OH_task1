from django.contrib import admin


from django.contrib import admin

from .models import Doc


class DocAdmin(admin.ModelAdmin):
    list_display = ('description', 'name', 'updated_at', 'link')


admin.site.register(Doc, DocAdmin)
