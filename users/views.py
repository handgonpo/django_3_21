# Django의 기본 기능들을 불러옵니다.
# - render: 템플릿 파일을 불러와서 HTML로 변환합니다.
# - redirect: 다른 URL로 이동(리다이렉트)할 때 사용합니다.
# - HttpResponse: HTTP 응답 객체를 생성해 반환합니다.
# - get_object_or_404: 데이터베이스에서 객체를 조회하고, 없으면 404 에러를 발생시킵니다.
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404

# models.py 파일에서 Topic 모델(데이터베이스 테이블에 대응하는 클래스)을 가져옵니다.
from .models import Topic

# CSRF 보호를 우회할 수 있도록 하는 데코레이터입니다.
from django.views.decorators.csrf import csrf_exempt


def HtmlTemplate(articleTag):
    """
    HTML 템플릿을 생성하는 함수입니다.
    - articleTag: 동적으로 추가할 콘텐츠(예: 본문, 폼 등)를 전달받습니다.
    - 이 함수는 데이터베이스에 저장된 모든 Topic 객체를 가져와서
      각 Topic의 제목과 상세 페이지로 연결되는 링크 목록(ul)을 만들어 HTML에 포함시킵니다.
    """
    # Topic 테이블의 모든 레코드를 가져옵니다.
    topics = Topic.objects.all()
    # 빈 문자열로 시작하는 HTML 리스트(li) 항목들을 저장할 변수입니다.
    ol = ""
    # 데이터베이스에 있는 모든 Topic 객체를 순회하며 리스트 항목을 만듭니다.
    for topic in topics:
        # 각 Topic의 id와 title을 사용하여 링크(li)를 만듭니다.
        ol += f"<li><a href='/read/{topic.id}/'>{topic.title}</a></li>"
    # 완성된 HTML 코드를 반환합니다.
    # - 상단에 제목(Django)을 표시하고, Topic 목록, 전달받은 articleTag(본문 혹은 폼),
    #   그리고 Create 페이지로 이동하는 링크를 포함합니다.
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
    """
    메인 페이지(index) 뷰 함수입니다.
    - 간단한 환영 메시지를 articleTag 변수에 저장하고, 이를 HTML 템플릿에 포함시켜 출력합니다.
    """
    # 간단한 환영 메시지와 함께 본문을 구성합니다.
    articleTag = """
    <h2>Welcome</h2>
    hello, Django
    """
    # HttpResponse를 사용해 완성된 HTML을 클라이언트에게 반환합니다.
    return HttpResponse(HtmlTemplate(articleTag))


def read(request, id):
    """
    특정 Topic의 상세 내용을 보여주는 뷰 함수입니다.
    - URL에 전달된 id 값을 사용해 해당 Topic 객체를 조회합니다.
    - 만약 해당 id에 해당하는 Topic이 없으면 404 에러 페이지를 띄웁니다.
    """
    # id에 해당하는 Topic 객체를 가져옵니다. 없으면 404 에러 발생!
    topic = get_object_or_404(Topic, pk=id)
    # Topic의 제목과 본문(body)을 포함한 HTML 문자열을 생성합니다.
    article = f"<h2>{topic.title}</h2>{topic.body}"
    # 완성된 HTML을 반환합니다.
    return HttpResponse(HtmlTemplate(article))


@csrf_exempt  # CSRF 보호를 비활성화합니다. (실제 서비스에서는 보안 이슈가 될 수 있으므로 주의!)
def create(request):
    """
    Article(Topic) 생성 페이지 뷰 함수입니다.
    
    - GET 요청 시:
      1. DB에 저장된 모든 Article(Topic)의 제목 목록을 보여주고,
      2. 새 Article을 등록할 수 있는 폼(form)을 제공합니다.
      
    - POST 요청 시:
      1. 폼에서 전달된 title(제목)과 body(본문) 데이터를 받아,
      2. 새로운 Article(Topic)을 데이터베이스에 생성한 후,
      3. 다시 /create/ 페이지로 리다이렉트하여 목록을 갱신합니다.
    """
    # 요청 방식(GET, POST 등)을 확인합니다.
    # print(request.method)  # 요청 방식을 콘솔에 출력할 수 있습니다.
    if request.method == "GET":
        # GET 요청: 사용자가 페이지에 접속했을 때, Article 등록 폼을 보여줍니다.
        
        # 데이터베이스에서 모든 Topic(Article) 객체를 가져옵니다.
        topics = Topic.objects.all()
        
        # 새 Article을 등록할 수 있는 HTML 폼을 작성합니다.
        article = """
            <form action="/create/" method="post">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit"></p>
            </form>
        """

        # 아래의 코드는 현재 DB에 저장된 Article들의 제목 목록을 만드는 예시입니다.
        # 하지만 HtmlTemplate 함수 내에서 이미 모든 Topic의 제목 목록을 보여주기 때문에
        # 실제로는 따로 사용되지 않습니다.
        topic_list = "<ul>"
        for t in topics:
            topic_list += f"<li>{t.title}</li>"
        topic_list += "</ul>"

        # 완성된 폼을 포함한 HTML을 반환합니다.
        return HttpResponse(HtmlTemplate(article))
    elif request.method == "POST":
        # POST 요청: 폼 제출 후, 새로운 Article(Topic)을 생성하는 과정입니다.
        
        # 폼으로부터 전송된 데이터를 추출합니다.
        # get 메서드를 사용하여 title과 body 값을 가져오며,
        # 해당 값이 없으면 빈 문자열("")을 기본값으로 사용합니다.
        title = request.POST.get("title", "")
        body = request.POST.get("body", "")

        # 추출한 데이터를 사용해 새 Topic 객체를 데이터베이스에 저장합니다.
        Topic.objects.create(title=title, body=body)

        # 새 Article 생성 후, /create/ 페이지로 이동(리다이렉트)하여 갱신된 목록을 보여줍니다.
        return redirect("/create/")
