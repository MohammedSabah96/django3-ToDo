from django.contrib import admin
from .models import Tasks
# Register your models here.

class ToDo(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Tasks, ToDo)