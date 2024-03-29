from django.utils import timezone
from django.views import generic

from .models import Author, Article, Tag


class AuthorIndexView(generic.ListView):
    template_name = 'django_articles/author_index.html'
    context_object_name = 'authors_list'

    def get_queryset(self):
        """
        Returns a query set that includes authors of published articles.
        """
        return Author.objects.all()
    

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'django_articles/author_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        articles = author.article_set.filter(
            pub_date__lte=timezone.now()
        ).exclude(
            title=''
        ).exclude(
            tags__isnull=True
        ).exclude(
            content=''
        )
        context['articles'] = articles
        return context


class ArticleIndexView(generic.ListView):
    template_name = 'django_articles/article_index.html'
    context_object_name = 'published_articles_list'

    def get_queryset(self):
        """
        Returns a query set that includes articles whose pub_date is present or past, and excludes articles with empty fields.
        """
        return Article.objects.filter(
            pub_date__lte=timezone.now()
        ).exclude(
            title=''
        ).exclude(
            tags__isnull=True
        ).exclude(
            content=''
        )
    

class ArticleDetailView(generic.DetailView):
    template_name = 'django_articles/article_detail.html'

    def get_queryset(self):
        """
        Returns article whose primary key is provided in the request.
        """
        search_request = self.request.resolver_match.kwargs.get('pk')
        return Article.objects.filter(
            pk=search_request,
            pub_date__lte=timezone.now()
        ).exclude(
            title=''
        ).exclude(
            tags__isnull=True
        ).exclude(
            content=''
        )


class TagIndexView(generic.ListView):
    template_name = 'django_articles/tag_index.html'
    context_object_name = 'available_tags_list'

    def get_queryset(self):
        """
        Returns query set of all tags in database.
        """
        return Tag.objects.all()
    

class TagRelationsIndexView(generic.ListView):
    template_name = 'django_articles/tag_relations_index.html'
    context_object_name = 'tag_relations_list'

    def get_queryset(self):
        """
        Returns a query set of articles whose tags contain the tag with primary key provided in the request, and excludes articles with empty fields.
        """
        search_request = self.request.resolver_match.kwargs.get('pk')
        return Article.objects.filter(
            tags__pk=search_request,
            pub_date__lte=timezone.now()
        ).exclude(
            title=''
        ).exclude(
            tags__isnull=True
        ).exclude(
            content=''
        )
