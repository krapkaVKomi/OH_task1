from django.shortcuts import render
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    checks_list = Checks.objects.all()
    query = request.GET.get('q')
    if query:
        checks_list = Checks.objects.filter(
            Q(name__icontains=query)).distinct()

    paginator = Paginator(checks_list, 2)  # 2 posts per page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts
    }
    return render(request, "main/index.html", context)
