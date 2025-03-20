from django.shortcuts import render, HttpResponse

topics = [
    {"id": 1, "title": "routing", "body": "Routing is..."},
    {"id": 2, "title": "view", "body": "View is..."},
    {"id": 3, "title": "model", "body": "Model is..."},
]


def HtmlTemplate(articleTag):
    global topics
    ol = ""
    for topic in topics:
        ol += f"<li><a href='/read/{topic["id"]}'>{topic['title']}</a></li>"
    return HttpResponse(
        f"""
        <html>
        <body>
            <h1>Django</h1>
            <ol>
                {ol}
            </ol>
            {articleTag}
        </body>
        </html>
        """
    )


def index(request):
    articleTag = """
    <h2>Welcom</h2>
    hello, Django
    """
    return HttpResponse(HtmlTemplate(articleTag))


def read(request, id):
    return HttpResponse("Hello, world. Read!" + id)


def create(request):
    return HttpResponse("Hello, world. Create!")
