from django.conf.urls import url

from . import views
app_name="develop"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dev_ind_data/$', views.dev_ind_data, name='dev_ind_data'),
]