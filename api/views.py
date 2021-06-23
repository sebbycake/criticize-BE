import json
# from simpletransformers.t5 import T5Model
from transformers import pipeline
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_page
from .scraper import Scraper
from .recommendations import get_json_data

# model_args = {
#     "reprocess_input_data": True,
#     "overwrite_output_dir": True,
#     "max_seq_length": 128,
#     "eval_batch_size": 16,
#     "num_train_epochs": 1,
#     "save_eval_checkpoints": False,
#     "use_multiprocessing": False,
#     # "silent": True,
#     "num_beams": None,
#     "do_sample": True,
#     "max_length": 50,
#     "top_k": 50,
#     "top_p": 0.95,
#     "num_return_sequences": 10,
# }

# MODEL = T5Model("t5", "outputs/best_model", args=model_args, use_cuda=False)

# @api_view(['POST'])
# def generate_questions(request):
#     try:
#         json_req = json.loads(request.body) 
#         article = json_req['article']
#         # concantenate with task prefix
#         query = "ask_question: " + article
#         # prefix output
#         preds = MODEL.predict([query])
#         qn_list = preds[0]
#         json_data = [{'id': index, 'question': qn} for index, qn in enumerate(qn_list, 1)]
#         return Response(json_data, status=200)
#     except KeyError:
#         return Response({"error": "Please input a news article content"}, status=400)

scraper = Scraper()

@cache_page(60 * 60)
@api_view(['GET'])
def scrape_articles(request):
    global global_articles 
    global_articles = scraper.get_source_and_title()
    return Response(global_articles, status=200)

@api_view(['POST'])
def get_related_articles(request):
    try:
        json_req = json.loads(request.body) 
        article_title = json_req['article_title']
        related_articles = get_json_data(global_articles, article_title)
        return Response(related_articles, status=200)
    except KeyError:
        return Response({"error": "Please input a news article content"}, status=400)
    except NameError:
        return Response({"error": "Get the top daily news first"}, status=400)


@api_view(['POST'])
def summarize_article(request):
    try:
        json_req = json.loads(request.body) 
        article = json_req['article'][:1024]
        summarizer = pipeline("summarization")
        summarized_article = summarizer(article, min_length=5, max_length=512)[0]
        return Response(summarized_article, status=200)
    except KeyError:
        return Response({"error": "Please input a news article content"}, status=400)


