from django.forms import ModelForm
from .models import Tasks

class ToDoForm(ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'memo', 'importand']