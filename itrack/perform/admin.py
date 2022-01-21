from django.forms.models import ModelForm
from .models import *
from django.contrib import admin


#https://stackoverflow.com/questions/3657709/how-to-force-save-an-empty-unchanged-django-admin-inline
class AlwaysChangedModelForm(ModelForm):
    def has_changed(self, *args, **kwargs):
        if self.instance.pk is None:
            return True
        return super(AlwaysChangedModelForm, self).has_changed(*args, **kwargs)


class Sop_policy_damage_mitigationInline(admin.TabularInline):
    model = Sop_policy_damage_mitigation
    extra = 0
    form = AlwaysChangedModelForm

class Sop_policyAdmin(admin.ModelAdmin):
    list_display = ('spid','Ds_level','Sop_policy','Measure_type','Measure_description','Prerequesit_sop_policy','Implementation_stage','Means_of_attack','Attack_context','Location','Mcda_criteria','Mcda_points','Implementation_cost','Cost_type','Measure_source',)
    #list_editable = ('Ds_level','Sop_policy','Measure_family','Measure_type','Measure_description','Prerequesit_sop_policy','Implementation_stage','Means_of_attack','Attack_context','Location','Mcda_criteria','Mcda_points','Implementation_cost','Cost_type','Measure_source',)
    list_filter = ('Location','Attack_context','Means_of_attack','Ds_level','Implementation_stage','Mcda_criteria',)
    search_fields = ('Measure_description','Location','Attack_context','Means_of_attack','Ds_level','Implementation_stage','Mcda_criteria',)
    inlines = [ Sop_policy_damage_mitigationInline, ]

class Sop_policy_damage_mitigationAdmin(admin.ModelAdmin):
    list_display  = ('spdmid','Damage_type','Damage_mitigation_fraction',)



class Sop_policySurveyQuestionAnswerInline(admin.TabularInline):
    model = Sop_policySurveyQuestionAnswer
    extra = 0
    form = AlwaysChangedModelForm


class Sop_policySurveyAnswerAdmin(admin.ModelAdmin):
    #list_display = ('usid',)
    #list_editable = ('','','',)
    #list_filter = ('usid',)
    #search_fields = ('usid',)
    inlines = [Sop_policySurveyQuestionAnswerInline, ]


admin.site.register(Sop_policySurveyAnswer,Sop_policySurveyAnswerAdmin)
admin.site.register(Sop_policy, Sop_policyAdmin)
#admin.site.register(Sop_policy_damage_mitigation,Sop_policy_damage_mitigationAdmin)
admin.site.register(PerformanceIndicator)
admin.site.register(PerformanceIndicatorValue)
admin.site.register(PerformanceIndicatorTaskTarget)
admin.site.register(PerformanceIndicatorTaskBenchmark)