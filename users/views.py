from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Topic

def index(request):
    # 모든 Topic을 가져와 템플릿으로 넘긴다.
    topics = Topic.objects.all()
    return render(request, 'users/index.html', {
        'topics': topics,  # base.html에서 사용
    })

def read(request, id):
    topic = get_object_or_404(Topic, pk=id)
    # base.html에서 topics 목록을 같이 쓰고 싶다면, 여기도 Topic.objects.all()을 보낼 수 있음
    topics = Topic.objects.all()
    return render(request, 'users/read.html', {
        'topic': topic,
        'topics': topics
    })

@csrf_exempt
def create(request):
    if request.method == 'GET':
        topics = Topic.objects.all()
        return render(request, 'users/create.html', {
            'topics': topics
        })
    elif request.method == 'POST':
        title = request.POST.get('title', '')
        body = request.POST.get('body', '')
        Topic.objects.create(title=title, body=body)
        return redirect('index')  # URL name으로 리다이렉트 (urls.py에서 name='index'로 설정 가정)
    
@csrf_exempt
def delete(request):
    if request.method == 'POST':
        topic_id = request.POST.get('id')
        topic = get_object_or_404(Topic, pk=topic_id)
        topic.delete()
    return redirect('index')
