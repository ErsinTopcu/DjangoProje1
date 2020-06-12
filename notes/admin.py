from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from notes.models import Category, LectureNote, Images, Comment


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
    prepopulated_fields = {'slug': ('title',)}


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'notes', 'image_tag']
    readonly_fields = ('image_tag',)


class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_LectureNote_count', 'related_LectureNote_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            LectureNote,
            'category',
            'LectureNote_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                                                LectureNote,
                                                'category',
                                                'notes_count',
                                                cumulative=False)
        return qs

    def related_LectureNote_count(self, instance):
        return instance.notes_count

    related_LectureNote_count.short_description = 'Related LectureNote (for this specific category)'

    def related_LectureNote_cumulative_count(self, instance):
        return instance.LectureNote_cumulative_count

    related_LectureNote_cumulative_count.short_description = 'Related LectureNote (in tree)'


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'notes', 'user', 'status']
    list_filter = ['status']


admin.site.register(Category, CategoryAdmin2)
admin.site.register(LectureNote, LectureNoteAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Comment, CommentAdmin)
