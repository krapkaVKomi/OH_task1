from django.contrib import admin

from .models import *


class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')


class DocAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated_at', 'link')


class LineOfDocAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')


class WordOfDocAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')


admin.site.register(Doc, DocAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(LineOfDoc, LineOfDocAdmin)
admin.site.register(WordOfDoc, WordOfDocAdmin)
