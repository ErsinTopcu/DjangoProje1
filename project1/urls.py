"""project1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('notes/', include('notes.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from home import views

urlpatterns = [

    path('', include('home.urls')),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('references/', views.references, name='refences'),
    path('faq/', views.faq, name='faq'),
    path('features/', views.features, name='features'),
    path('home/', include('home.urls')),
    path('notes/', include('notes.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('category/<int:id>/<slug:slug>/', views.category_notes, name='category_notes'),
    path('LectureNotes/<int:id>/<slug:slug>/', views.notes_detail, name='notes_detail'),
    path('search/', views.notes_search, name='notes_search'),
    path('search_auto/', views.notes_search_auto, name='notes_search_auto'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
