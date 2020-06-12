import json
from unicodedata import category

from django.contrib.auth import logout, authenticate, login

import notes
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormMessage, ContactForm, UserProfile

from notes.models import LectureNote, Category, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = LectureNote.objects.all()[:4]
    category = Category.objects.all()
    lastnotes = LectureNote.objects.all().order_by('-id')[:3]
    randomnotes = LectureNote.objects.all().order_by('?')[:3]

    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'sliderdata': sliderdata,
               'randomnotes': randomnotes,
               'lastnotes': lastnotes
               }
    return render(request, 'index.html', context)


def about(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'category': category, 'page': 'about'}
    return render(request, 'about.html', context)


def features(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'category': category, 'page': 'features'}
    return render(request, 'features.html', context)


def faq(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'category': category, 'page': 'faq'}
    return render(request, 'faq.html', context)


def contact(request):
    if request.method == 'POST':  # form post edildiyse
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # model ile bağlantı kur
            data.name = form.cleaned_data['name']  # formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # veritabanına kaydet
            messages.success(request, "Your message send successfully. Thank you.")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    form = ContactForm()
    context = {'setting': setting, 'category': category, 'form': 'form'}
    return render(request, 'contact.html', context)


def references(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'category': category, 'page': 'references'}
    return render(request, 'references.html', context)


def category_notes(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    notes = LectureNote.objects.filter(category_id=id)
    context = {'notes': notes,
               'category': category,
               'categorydata': categorydata,
               }
    return render(request, 'notes.html', context)


def notes_detail(request, id, slug):
    mesaj = "Ders Notu ", id, "/", slug
    category = Category.objects.all()
    notes = LectureNote.objects.get(pk=id)
    images = Images.objects.filter(notes_id=id)
    comments = Comment.objects.filter(notes_id=id, status='True')
    context = {'notes': notes,
               'category': category,
               'images': images,
               'comments': comments,

               }
    return render(request, 'notes_detail.html', context)


def notes_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            search = form.cleaned_data["search"]
            catid = form.cleaned_data["catid"]
            if catid == 0:
                notes = LectureNote.objects.filter(title__icontains=search)
            else:
                notes = LectureNote.objects.filter(title__icontains=search, category_id=catid)

            context = {'notes': notes,
                       'category': category,
                       }
            return render(request, 'notes_search.html', context)

    return HttpResponseRedirect('/')


def notes_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        notes = LectureNote.objects.filter(title__icontains=q)
        results = []
        for rs in notes:
            notes_json = {}
            notes_json = rs.title
            results.append(notes_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Hatası! Kullanıcı Adı veya Şifre Yanlış")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {'category': category,
               }
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, "Hoş Geldiniiz,Başarılı bir şeklilde kayıt oldunuz.")
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
               }
    return render(request, 'signup.html', context)
