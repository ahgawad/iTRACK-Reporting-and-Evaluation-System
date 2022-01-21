from django.contrib import admin
from django.forms.models import ModelForm



admin.site.site_header = 'iTRACK Reporting and Evaluation System - administration'
admin.site.site_title = 'iTRACK Reporting and Evaluation System - administration'
admin.site.index_title = 'iTRACK Reporting and Evaluation System - administration'


#https://stackoverflow.com/questions/3657709/how-to-force-save-an-empty-unchanged-django-admin-inline
class AlwaysChangedModelForm(ModelForm):
    def has_changed(self, *args, **kwargs):
        if self.instance.pk is None:
            return True
        return super(AlwaysChangedModelForm, self).has_changed(*args, **kwargs)

