from django.shortcuts import render
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def document_save(request):
    if request.method == "POST":
        doc = request.FILES["file"]
        link = "D:\\Users\\User\\Have_to\\one\\find\\media\\" + doc.name
        doc_file = Doc.objects.create(name=doc.name, file=doc, link=link)
        doc_path = doc_file.file.path
        return render(request, "main/test.html", {"doc_path": doc_path})
    return render(request, "main/test.html")


def index(request):
    checks_list = Doc.objects.all()
    query = request.GET.get('q')
    if query:
        checks_list = Doc.objects.filter(
            Q(name__icontains=query)).distinct()

    paginator = Paginator(checks_list, 5)  # 5 posts per page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
    }
    return render(request, "main/index.html", context)
