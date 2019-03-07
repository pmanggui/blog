from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Blog
from .form import BlogPost

# Create your views here.

def home(request):
    blogs = Blog.objects # 쿼리셋 
    #블로그 모든 글들을 대상으로 
    blog_list = Blog.objects.all()
    #블로그 객체 세 개를 한페이지로 자르기
    paginator = Paginator(blog_list, 3)
    #request된 페이지가 무너지를 알아내고( request 페이지를 변수에 담아내고)
    page = request.GET.get('page')
    #request된 페이지를 얻어온 뒤 return 해 준다
    posts = paginator.get_page(page)
    # 메소드: 기능 첨부  
    return render(request, 'home.html', {'blogs': blogs, 'posts': posts})

    #쿼리셋과 메소드의 형식
    #모델.쿼리셋(objects).메소드

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk = blog_id)

    return render(request, 'detail.html', {'blog':blog_detail})

def new(request):
    return render(request, "new.html")

def create(request):
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()
    return redirect('/blog/'+str(blog.id)) #render와 차이 어떤 상황에서 사용하냐
    #redirect는 url을 전혀 다른 url(ex. https://google.com)을 지정할 수 있음

def blogpost(request):
    #1. 입력된 내용을 처리하는 기능 -> POST
    if request.method == 'POST':
        form = BlogPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.save()
            return redirect('home')
        
    #2. 빈 페이지를 띄워주는 기능 -> GET
    else:
        form = BlogPost()
        return render(request, 'new.html', {'form':form})

def delete(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    blog.delete()
    return redirect('home')

def update(request, blog_id):
    blog_update = Blog.objects.get(id=blog_id)
    if request.method == 'POST':
        if request.method == 'POST':
            blog_update.title = request.POST['title']
            blog_update.body = request.POST['body']
            blog_update.pub_date = timezone.datetime.now()
            blog_update.save()
            return redirect('detail', blog_id)

    else :
        return render(request, 'update.html', {'blog':blog_update})