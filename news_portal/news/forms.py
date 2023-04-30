from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Post


class NewForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'category', 'title', 'post_text']

    def clean(self):
        cleaned_data = super().clean()
        post_text = cleaned_data.get("post_text")
        title = cleaned_data.get("title")

        if title == post_text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data