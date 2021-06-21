from django.contrib import admin
from django.urls import path
from api.views import generate_questions
from api.views import scrape_articles
from api.views import summarize_article
from api.views import get_related_articles

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/questions', generate_questions),
    path('v1/articles', scrape_articles),
    path('v1/related-articles', get_related_articles),
    path('v1/summary', summarize_article),
]
