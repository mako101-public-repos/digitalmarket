from django.contrib import admin

# Register your models here.
from analytics.models import TagView


@admin.register(TagView)
class TagViewAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active']

    class Meta:
        model = TagView
