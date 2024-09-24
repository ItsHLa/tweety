from django_filters.filterset import FilterSet
import django_filters
from tweety_posts.models import Post

class PostFilter(FilterSet):
    content = django_filters.CharFilter(field_name="content",lookup_expr="icontains")
    date = django_filters.DateFromToRangeFilter()
    class Meta:
        model = Post
        fields = ["author" ,"content","date"]