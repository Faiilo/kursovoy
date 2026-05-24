from django.contrib import admin
from .models import DatasetOtchet, PracType, DocumentTemplate

class DocumentTemplateAdmin(admin.ModelAdmin):
    list_display = ('doc_type', 'name', 'uploaded_at')
    fieldsets = ((None, {'fields': ('doc_type', 'name', 'template_file')}),)
    
    def save_model(self, request, obj, form, change):
        if not change:
            DocumentTemplate.objects.filter(doc_type=obj.doc_type).delete()
        super().save_model(request, obj, form, change)

admin.site.register(DatasetOtchet)
admin.site.register(PracType)
admin.site.register(DocumentTemplate, DocumentTemplateAdmin)