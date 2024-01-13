from django.forms import IntegerField, ModelForm, ModelMultipleChoiceField, TextInput

from .models import Category, Title


class CreateTitlesForm(ModelForm):
    categories = ModelMultipleChoiceField(queryset=Category.objects.all())
    number_of_titles = IntegerField(
        widget=TextInput(attrs={'placeholder': "default value set to 30"}),
        required=False,
    )

    class Meta:
        model = Title
        fields = ["categories", "number_of_titles"]
