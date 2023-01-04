from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserLoginForm
from datetime import datetime


@login_required
def index(request):
    if request.method == "POST":
        doc = request.FILES["file"]

        doc_file = Doc.objects.create(name=doc.name, file=doc)
        doc_path = doc_file.file.path
        doc_type = doc.name.split('.')
        doc_type = doc_type[-1]
        if doc_type == 'txt':
            with open(doc_path, 'r', encoding="utf-8") as file:
                line_count = 1
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
                        word = word.strip()
                        if len(word) > 3:
                            words_of_line.append(word)
                            line += word + ' '

                    line_of_doc = LineOfDoc.objects.create(text=line, doc=doc_file, line_number=line_count)
                    line_count += 1
                    line = line.split(' ')
                    for word in line:
                        WordOfDoc.objects.create(text=word, line=line_of_doc, doc=doc_file)
            doc_path = doc_file.file.path
            render(request, "main/index.html", {"doc_path": doc_path})
            return redirect('/')

        else:
            print("ПОМИЛКА ", doc_type)
    else:
        start = datetime.now()
        docs = Doc.objects.all()
        if len(docs) != 0:
            list_of_docs = {'docs': docs}
        else:
            list_of_docs = {'docs': False}
        query = request.GET.get('q')

        get_docs = []

        for item in docs:

            select_file = request.GET.get(str(item))
            if select_file:
                get_docs.append(select_file)

        #print(get_docs)

        if query:
            docs = []
            for doc in get_docs:
                select_file_id = Doc.objects.filter(name=doc)[0:]
                select_file_id = select_file_id.values('id').get()
                select_file_id = select_file_id['id']
                words_filter_docs = WordOfDoc.objects.filter(doc_id=select_file_id)
                for i in words_filter_docs:
                    docs.append(i)

            word_filter = WordOfDoc.objects.filter(text=query)
            arr = []
            for i in word_filter:
                for j in docs:
                    print(i, ' + ', j)
                    if i == j:
                        arr.append(j)
            # віджет тепер інший, тепер Get запит виглядає інакше i пагінація знову зломана

            # paginator = Paginator(arr, 30)
            # page = request.GET.get('page')
            #
            # try:
            #     posts = paginator.page(page)
            # except PageNotAnInteger:
            #     posts = paginator.page(1)
            # except EmptyPage:
            #     posts = paginator.page(paginator.num_pages)

            context = {
                'table': True,
                'posts': arr,
                'list_of_docs': list_of_docs
            }
            duration = datetime.now() - start
            print('Виконання завершено!')
            print(f'Тривалість: {duration}')
            return render(request, "main/index.html", context)

        else:
            context = {'table': False,
                       'list_of_docs': list_of_docs
                       }
            return render(request, "main/index.html", context)


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
