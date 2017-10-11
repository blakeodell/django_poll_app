from django.contrib import admin

from .models import Question, Choice

# Register your models here.
#admin.site.register(Question) #Inital registration/default

#class QuestionAdmin(admin.ModelAdmin):  #puts multiple fields on the form
#    fields = ['pub_date', 'question_text']

#admin.site.register(Question, QuestionAdmin)



#class ChoiceInline(admin.StackedInline): #displays stacked
class ChoiceInline(admin.TabularInline): #displays tabular
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,        {'fields': ['question_text']}),
        ('Date Info', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently', 'get_choices')
    #list_display = ('question_text', 'pub_date', 'was_published_recently')

    list_filter = ['pub_date']
    search_fields = ['question_text', 'get_choices']

admin.site.register(Question, QuestionAdmin)