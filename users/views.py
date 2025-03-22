from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Topic

def HtmlTemplate(articleTag):
    topics = Topic.objects.all()
    ol = ""
    for topic in topics:
        ol += f"<li><a href='/read/{topic.id}/'>{topic.title}</a></li>"
    return f"""
        <html>
        <body>
            <h1>Django</h1>
            <ul>
                {ol}
            </ul>
            {articleTag}
        </body>
        </html>
    """

def index(request):
    articleTag = """
    <h2>Welcome</h2>
    hello, Django
    """
    return HttpResponse(HtmlTemplate(articleTag))

def read(request, id):
    topic = get_object_or_404(Topic, pk=id)
    article = f"<h2>{topic.title}</h2>{topic.body}"
    return HttpResponse(HtmlTemplate(article))

def create(request):
    return HttpResponse("Hello, world. Create!")
