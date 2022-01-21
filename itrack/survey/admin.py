from django.contrib import admin
from django.forms.models import ModelForm

# Register your models here.
from .models import UserSurvey, UserSurveyQuestion, UserSurveyAnswer ,UserSurveyQuestionAnswer, UserSurveyQuestionConstruct

#https://stackoverflow.com/questions/3657709/how-to-force-save-an-empty-unchanged-django-admin-inline
class AlwaysChangedModelForm(ModelForm):
    def has_changed(self, *args, **kwargs):
        if self.instance.pk is None:
            return True
        return super(AlwaysChangedModelForm, self).has_changed(*args, **kwargs)


class UserSurveyQuestionInline(admin.TabularInline):
    model = UserSurveyQuestion
    extra = 0
    form = AlwaysChangedModelForm


class UserSurveyAdmin(admin.ModelAdmin):
    list_display = ('survey_name',)
    #list_editable = ('','','',)
    list_filter = ('survey_name',)
    search_fields = ('survey_name',)
    inlines = [ UserSurveyQuestionInline, ]


class UserSurveyQuestionAnswerInline(admin.TabularInline):
    model = UserSurveyQuestionAnswer
    extra = 0
    form = AlwaysChangedModelForm
    '''
    def get_queryset(self, request):
        qs = super(UserSurveyQuestionAnswerInline, self).get_queryset(request)
        #UserSurvey, UserSurveyQuestion, UserSurveyAnswer ,UserSurveyQuestionAnswer, UserSurveyQuestionConstruct
        qs1 = UserSurveyAnswer.objects.all()
        qs2 = UserSurveyQuestion.objects.all()
        qs3 =UserSurvey.objects.all()
        return qs #.filter(usqid=2)
    '''

class SurveyAnswerAdmin(admin.ModelAdmin):
    #list_display = ('usid',)
    #list_editable = ('','','',)
    #list_filter = ('usid',)
    #search_fields = ('usid',)
    inlines = [UserSurveyQuestionAnswerInline, ]


admin.site.register(UserSurvey,UserSurveyAdmin)
admin.site.register(UserSurveyQuestionConstruct)
admin.site.register(UserSurveyAnswer,SurveyAnswerAdmin)
