import django_filters
from django_filters import FilterSet, DateTimeFilter
from .models import Post
from django.forms import DateTimeInput


class PostFilter(FilterSet):
    article = django_filters.ChoiceFilter(label='Тип', choices=Post.articl, empty_label=' ')
    heading = django_filters.CharFilter(label='Заголовок', lookup_expr='icontains')
    added_after = DateTimeFilter(
        field_name='date_of_creation',
        lookup_expr='gt',
        label='Дата создания (не позднее)',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'date'},
        ),
    )



