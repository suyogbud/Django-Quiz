from django.contrib import admin

from .models import Choice, Question

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?"
    )
    def was_published_recently(self, obj):
        return obj.was_published_recently()
    
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    (None, {"fields": ["question_text"]}),
    ("Date information", {"fields": ["pub_date"], "classes":["collapse"]}),
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)