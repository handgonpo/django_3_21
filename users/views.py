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
            <ul>
                {ol}
            </ul>
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
    global topics
    article = ""

    # id를 정수형으로 변환
    id = int(id)

    for topic in topics:
        print(topic["id"], type(id))
        if topic["id"] == id:
            article = f'<h2>{topic["title"]}<h2>{topic["body"]}'
            return HttpResponse(HtmlTemplate(article))
    return HttpResponse("Hello, world. Read!" + id)


def create(request):
    return HttpResponse("Hello, world. Create!")
