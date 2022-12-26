from django.contrib import admin


from django.contrib import admin

from .models import Doc, Document, LineOfDoc, WordOfDoc


class DocAdmin(admin.ModelAdmin):
    list_display = ('description', 'name', 'updated_at', 'link')


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class LineOfDocAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')


class WordOfDocAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')


admin.site.register(Doc, DocAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(LineOfDoc, LineOfDocAdmin)
admin.site.register(WordOfDoc, WordOfDocAdmin)
