from rest_framework import generics
import requests
from .models import News
from .serializers import NewsSerializer
from django.conf import settings
from rest_framework.response import Response
from .utils import threaded

class NewsList(generics.ListAPIView):  

    queryset = News.objects.all()
    serializer_class = NewsSerializer
    api_key = settings.API_KEY

    @threaded
    def create_news(self, articles, query):
        News.objects.bulk_create([
            News(
                title=article["title"],
                description=article["description"],
                query=query,
                author=article["author"],
                content=article["content"],
                published_at=article["publishedAt"],
                url=article["url"],
            ) for article in articles
        ])

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        category = request.GET.get('category')
        country = request.GET.get('country')

        if query:
            queryset = News.objects.filter(query=query)
        elif category:
            queryset = News.objects.filter(category=category)
        elif country:
            queryset = News.objects.filter(country=country)
        else:
            return Response({"error": "Provide query, category, or country parameter"})

        if queryset.exists():
            print("db")
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            print("api")
            api_key = self.api_key
            if query:
                url = f'https://newsapi.org/v2/everything?q={query}&apiKey={api_key}'
            elif category:
                url = f'https://newsapi.org/v2/top-headlines?q={category}&apiKey={api_key}'
            else:
                url = f'https://newsapi.org/v2/top-headlines?q={country}&apiKey={api_key}'

            response = requests.get(url)
            data = response.json()
            self.create_news(data["articles"], query or category or country)
            return Response(data)
