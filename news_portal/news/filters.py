from django_filters import FilterSet

from .models import Post

class NewsFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'date_time_create': ['gt'],
            'title': ['icontains'],
            'author': ['exact'],
        }