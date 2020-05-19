from unicodedata import category

import notes
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactFormMessage, ContactForm

from notes.models import LectureNote, Category


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = LectureNote.objects.all()[:4]
    category = Category.objects.all()
    lastnotes= LectureNote.objects.all().order_by('-id')[:3]
    randomnotes= LectureNote.objects.all().order_by('?')[:3]

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
               'categorydata':categorydata,
               }
    return render(request, 'notes.html', context)
