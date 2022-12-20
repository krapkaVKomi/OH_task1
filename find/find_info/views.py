from django.shortcuts import render
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def document_save(request):
    if request.method == "POST":
        doc = request.FILES["file"]

        doc_file = Document.objects.create(name=doc.name, file=doc)
        doc_path = doc_file.file.path
        doc_type = doc.name.split('.')
        doc_type = doc_type[-1]

        description = []
        with open(doc_path, 'r', encoding="utf-8") as file:
            for line in file:
                words = line.strip().split(' ')
                description.append(words)

        about_file = ''

        if len(description) != 0:
            for i in description[0]:
                about_file += i + ' '

        doc_file = Doc.objects.create(name=doc.name, file=doc, link=doc_path,
                                      description=description, about_file=about_file)
        doc_path = doc_file.file.path
        return render(request, "main/test.html", {"doc_path": doc_path})
    return render(request, "main/test.html")


def index(request):
    checks_list = Doc.objects.order_by('-id')
    query = request.GET.get('q')
    if query:
        checks_list = Doc.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)).distinct()

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
