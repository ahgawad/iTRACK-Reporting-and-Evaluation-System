from django.conf.urls import url

from . import views
app_name="survey"

urlpatterns = [
    url(r'^$', views.surveyentry, name='surveyshow'),
    url(r'^surveyentry/$', views.surveyentry, name='surveyentry'),
    url(r'^surveyshow/$', views.surveyshow, name='surveyshow'),
    url(r'^sur_charts_data/$', views.sur_charts_data, name='sur_charts_data'),
    url(r'^sur_questions_data/$', views.sur_questions_data, name='sur_questions_data'),
    url(r'^sur_entry_data/$', views.sur_entry_data, name='sur_entry_data'),
]