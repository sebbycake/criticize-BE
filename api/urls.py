from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('v1/articles', views.scrape_articles),
    path('v1/related-articles', views.get_related_articles),
    path('v1/summary', views.summarize_article),
]
