from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Topic
from django.views.decorators.csrf import csrf_exempt


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
            <ul>
                <li><a href="/create/">Create</a></li>
            </ul>
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


@csrf_exempt
def create(request):
    article = """
    <form action="/create/" method="post">
        <p><input type="text" name="title" placeholder="title"></p>
        <p><textarea name="body" placeholder="body"></textarea></p>
        <p><input type="submit"></p>
    </form>
"""
    return HttpResponse(HtmlTemplate(article))
