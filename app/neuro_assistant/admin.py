from django.contrib import admin
from .models import Category, Chunk

class ChunkAdmin(admin.ModelAdmin):
    list_display = ['short_text', 'category']
    list_filter = ['category']
    
    def short_text(self, obj):
        if len(obj.text) > 50:
            return obj.text[:50] + '...'
        else:
            return obj.text

admin.site.register(Chunk, ChunkAdmin)
admin.site.register(Category)
