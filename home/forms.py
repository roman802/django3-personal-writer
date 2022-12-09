from django.forms import ModelForm
from .models import Diskus

class BlogForm(ModelForm):
    class Meta:
        model = Diskus
        fields = ['memo']