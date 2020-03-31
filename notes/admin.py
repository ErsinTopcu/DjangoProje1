from django.contrib import admin

# Register your models here.
from notes.models import Category, LectureNote, Images


class LectureNoteImageInline(admin.TabularInline):
    model = Images
    extra = 3


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'image_tag']
    list_filter = ['status']
    readonly_fields = ('image_tag',)


class LectureNoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'image_tag', 'status']
    list_filter = ['status', 'category']
    inlines = [LectureNoteImageInline]
    readonly_fields = ('image_tag',)


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'notes', 'image_tag']
    readonly_fields = ('image_tag',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(LectureNote, LectureNoteAdmin)
admin.site.register(Images, ImagesAdmin)
