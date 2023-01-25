from django.shortcuts import render, redirect
from django.views.generic import View
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserLoginForm, NameForm
from chardet.universaldetector import UniversalDetector
from django.http import HttpResponseBadRequest, JsonResponse
from PyPDF2 import PdfReader
import json
import docx
import csv


def encoding(path):
    detector = UniversalDetector()
    with open(path, 'rb') as fh:
        for line in fh:
            detector.feed(line)
            if detector.done:
                break
        detector.close()

    return detector.result['encoding']


@login_required
def index(request):
    try:
        checkboxs = Checkbox.objects.filter(user=request.user.id).order_by('-pk')[0]
    except IndexError:
        checkboxs = None

    if checkboxs:
        checkboxs = str(checkboxs.session)[1:-1]
        checkboxs = checkboxs.replace("'", "").split(', ')

    if request.method == "POST":
        doc = request.FILES["file"]
        doc_type = doc.name.split('.')
        doc_type = doc_type[-1]

        form_doc_name = NameForm(request.POST)
        doc_name = form_doc_name['your_name'].value()
        docs = Doc.objects.all()
        status = True
        for name in docs:
            if str(name) == doc_name:
                status = False
                break

        if status and doc_type == 'txt':
            doc_file = File.objects.create(name=doc.name, file=doc)
            doc_path = doc_file.file.path
            document = Doc.objects.create(name=doc_name, link=doc_path)
            encod = encoding(path=doc_path)
            with open(doc_path, 'r', encoding=encod) as txt:
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

                    for word in words:
                        word = word.strip()
                        if len(word) > 3:
                            words_of_line.append(word)

                    line_of_doc = LineOfDoc.objects.create(text=line, doc=document, line_number=line_count)
                    line_count += 1
                    line = line.split(' ')
                    for word in line:
                        WordOfDoc.objects.create(text=word, line=line_of_doc, doc=document)
            render(request, "main/index.html", {"doc_path": doc_path})
            return redirect('/')

        elif status and doc_type == 'docx':
            doc_file = File.objects.create(name=doc.name, file=doc)
            doc_path = doc_file.file.path
            document = Doc.objects.create(name=doc_name, link=doc_path)
            doc = docx.Document(doc_path)
            line_count = 1
            for i in range(len(doc.paragraphs)):
                line = doc.paragraphs[i].text
                words = line.strip() \
                    .replace('\t', '') \
                    .replace('.', '') \
                    .replace(',', '') \
                    .replace('!', '') \
                    .replace('?', '') \
                    .replace('  ', ' ').split(' ')

                words_of_line = []
                for word in words:
                    word = word.strip()
                    if len(word) > 3:
                        words_of_line.append(word)

                line_of_doc = LineOfDoc.objects.create(text=line, doc=document, line_number=line_count)
                line_count += 1
                line = line.split(' ')
                for word in line:
                    WordOfDoc.objects.create(text=word, line=line_of_doc, doc=document)

            render(request, "main/index.html", {"doc_path": doc_path})
            return redirect('/')

        elif status and doc_type == 'csv':
            doc_file = File.objects.create(name=doc.name, file=doc)
            doc_path = doc_file.file.path
            document = Doc.objects.create(name=doc_name, link=doc_path)
            encod = encoding(path=doc_path)
            lines = []

            with open(doc_path, 'r', encoding=encod) as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    lines.append(row[0])

            line_count = 1
            for line in lines:
                words = line.strip() \
                    .replace('\t', '') \
                    .replace('.', '') \
                    .replace(',', '') \
                    .replace('!', '') \
                    .replace('?', '') \
                    .replace(';', '') \
                    .replace('\n', '') \
                    .replace('  ', ' ').split(' ')
                line_of_doc = LineOfDoc.objects.create(text=line, doc=document, line_number=line_count)
                for word in words:
                    WordOfDoc.objects.create(text=word, line=line_of_doc, doc=document)
                line_count += 1

            render(request, "main/index.html", {"doc_path": doc_path})
            return redirect('/')

        elif status and doc_type == 'pdf':
            doc_file = File.objects.create(name=doc.name, file=doc)
            doc_path = doc_file.file.path
            document = Doc.objects.create(name=doc_name, link=doc_path)
            reader = PdfReader(doc_path)

            number_of_pages = len(reader.pages)
            for i in range(number_of_pages):
                page = reader.pages[i]
                lines_of_page = page.extract_text().split('\n')
                line_count = 1
                for line in lines_of_page:
                    line_of_doc = LineOfDoc.objects.create(text=line, doc=document, line_number=line_count)
                    line_count += 1
                    line = line.strip() \
                        .replace('\t', '') \
                        .replace('.', '') \
                        .replace(',', '') \
                        .replace('!', '') \
                        .replace('?', '') \
                        .replace('  ', ' ').split(' ')
                    for word in line:
                        if len(word) > 3:
                            WordOfDoc.objects.create(text=word, line=line_of_doc, doc=document)

        else:
            print("ПОМИЛКА ", doc_type, doc_name)
            return redirect('/')
    else:
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
                if checkboxs:
                    for i in docs:
                        if i.name not in checkboxs:
                            doc_arr.append(i.name)
                else:
                    for i in docs:
                        doc_arr.append(i.name)

            if checkboxs != None and len(checkboxs) != 0:
                list_of_docs = {'docs': doc_arr,
                                'checkboxs': checkboxs}

            else:
                arr = []
                for i in docs:
                    arr.append(i.name)
                list_of_docs = {'docs': arr,
                                'checkboxs': False}
        else:
            list_of_docs = None

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

                lines_of_tible = WordOfDoc.objects.filter(doc_id=select_file_id) & WordOfDoc.objects.filter(text__istartswith=query)
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
                    start = f'{int(page)-1}'
                    if start != '0':
                        if paginator.page_range.stop - int(page) > 10:
                            page = f'{start}:{int(page)+10}'
                        else:
                            page = f'{paginator.page_range.stop - 10}:{paginator.page_range.stop}'

                    else:
                        page = f'{int(page)}:{int(page) + 10}'

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


#class TaskList(View):

#    def get(self, request):
#        return render(request, 'main/test.html')


def todos(request):
    print(request)
    # request.is_ajax() is deprecated since django 3.1
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'GET':
            print(request.method, ')) GET')
            todos = list(WordOfDoc.objects.all().values())
            return JsonResponse({'context': todos})
        if request.method == 'POST':
            print(request.method, ')) POST')
            data = json.load(request)
            todo = data.get('payload')
            WordOfDoc.objects.create(task=todo['task'], completed=todo['completed'])
            return JsonResponse({'status': 'Todo added!'})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        # return HttpResponseBadRequest('Invalid request')
        return render(request, 'main/test.html')
