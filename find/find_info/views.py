from django.shortcuts import render, redirect
from .models import *
# from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserLoginForm


@login_required
def document_save(request):
    if request.method == "POST":
        doc = request.FILES["file"]

        doc_file = Doc.objects.create(name=doc.name, file=doc)
        doc_path = doc_file.file.path
        doc_type = doc.name.split('.')
        doc_type = doc_type[-1]
        if doc_type == 'txt':
            with open(doc_path, 'r', encoding="windows-1251") as file:
                for line in file:
                    words = line.strip() \
                        .replace('\t', '') \
                        .replace('.', '') \
                        .replace(',', '') \
                        .replace('!', '') \
                        .replace('?', '') \
                        .replace(';', '').split(' ')

                    words_of_line = []
                    line = ''
                    for word in words:
                        if len(word) > 3:
                            words_of_line.append(word)
                            line += word + ' '

                    line_of_doc = LineOfDoc.objects.create(text=line, doc=doc_file)
                    line = line.split(' ')
                    for word in line:
                        WordOfDoc.objects.create(text=word, line=line_of_doc)
            doc_path = doc_file.file.path
            return render(request, "main/test.html", {"doc_path": doc_path})

        else:
            print("ПОМИЛКА ", doc_type)
    return render(request, "main/test.html")


@login_required
def index(request):
    words = WordOfDoc.objects.order_by()
    query = request.GET.get('q')
    if query:
        words = WordOfDoc.objects.filter(text=query)  # .all().values()
        for word in words:
            line = LineOfDoc.objects.filter(text=word)


        paginator = Paginator(words, 1)  # 5 posts per page
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {
            'posts': posts,
            'words': words
        }
        return render(request, "main/index.html", context)
    else:
        return render(request, "main/index.html")



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Реєстрація успішна')
            return redirect('/')
        else:
            messages.error(request, 'Помилка реєстрації')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = UserLoginForm()
    return render(request, 'main/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('/')
