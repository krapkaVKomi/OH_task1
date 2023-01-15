from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserLoginForm, NameForm
from datetime import datetime


@login_required
def index(request):
    checkboxs = Checkbox.objects.filter(user=request.user.id).order_by('-pk')[0]
    checkboxs = str(checkboxs.session)[1:-1]
    checkboxs = checkboxs.replace("'", "").split(', ')

    if request.method == "POST":
        doc = request.FILES["file"]
        doc_type = doc.name.split('.')
        doc_type = doc_type[-1]
        if doc_type == 'txt':
            form_doc_name = NameForm(request.POST)
            doc_name = form_doc_name['your_name'].value()
            doc_file = File.objects.create(name=doc.name, file=doc)
            doc_path = doc_file.file.path
            document = Doc.objects.create(name=doc_name, link=doc_path)
            with open(doc_path, 'r', encoding="utf-8") as txt:
                line_count = 1
                for line in txt:
                    words = line.strip() \
                        .replace('\t', '') \
                        .replace('.', '') \
                        .replace(',', '') \
                        .replace('!', '') \
                        .replace('?', '') \
                        .replace('  ', ' ').split(' ')

                    words_of_line = []
                    line = ''
                    for word in words:
                        word = word.strip()
                        if len(word) > 3:
                            words_of_line.append(word)
                            line += word + ' '

                    line_of_doc = LineOfDoc.objects.create(text=line, doc=document, line_number=line_count)
                    line_count += 1
                    line = line.split(' ')
                    for word in line:
                        WordOfDoc.objects.create(text=word, line=line_of_doc, doc=document)
            render(request, "main/index.html", {"doc_path": doc_path})
            return redirect('/')

        else:
            print("ПОМИЛКА ", doc_type)
    else:
        start = datetime.now()
        docs = Doc.objects.all()
        get_docs = []

        for item in docs:
            select_file = request.GET.get(str(item))
            if select_file:
                get_docs.append(select_file)

        if len(docs) != 0:
            doc_arr = []

            if get_docs:
                checkboxs = get_docs
                for i in docs:
                    if i.name not in checkboxs:
                        doc_arr.append(i.name)

            else:
                for i in docs:
                    if i.name not in checkboxs:
                        doc_arr.append(i.name)


            if len(checkboxs) != 0:
                print(doc_arr)
                print(checkboxs)
                list_of_docs = {'docs': doc_arr,
                                'checkboxs': checkboxs}
            else:
                arr = []
                for i in docs:
                    arr.append(i.name)
                list_of_docs = {'docs': arr,
                                'checkboxs': False}
        else:
            list_of_docs = {'docs': False}

        query = request.GET.get('q')
        if get_docs:
            session = Checkbox.objects.create(user=request.user.id, session=get_docs)

        page = request.GET.get('page')

        if query:
            all = []
            for doc in get_docs:
                select_file_id = Doc.objects.filter(name=doc)[0:]
                select_file_id = select_file_id.values('id').get()
                select_file_id = select_file_id['id']

                #count_in_doc = (WordOfDoc.objects.filter(doc_id=select_file_id) & WordOfDoc.objects.filter(text=query)).count()

                lines_of_tible = WordOfDoc.objects.filter(doc_id=select_file_id) & WordOfDoc.objects.filter(text=query)
                for i in lines_of_tible:
                    all.append(i)


            paginator = Paginator(all, 30)  # 30 posts per page


            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)

            search = ''
            for i in get_docs:
                search += f"&{i}={i}"

            if page:
                if paginator.page_range.stop > 10:
                    page = f'{int(page)-1}:{int(page)+10}'

                elif paginator.page_range.stop <= 10:
                    page = f'{int(page)-1}:{paginator.page_range.stop}'

            else:
                page = f'1:10'

            context = {
                'search': search,
                'table': True,
                'posts': posts,
                'page': page,
                'list_of_docs': list_of_docs,
                'page_num': page
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
            messages.success(request, 'Registration is successful')
            return redirect('/')
        else:
            messages.error(request, 'Registration error')
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
