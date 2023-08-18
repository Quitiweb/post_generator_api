from django.forms import FileField, ModelForm, SelectDateWidget

from .models import Title


class CreateTitlesForm(ModelForm):
    # csv_file = FileField()

    class Meta:
        model = Title
        fields = ["name", "category", "used"]
        # widgets = {}
