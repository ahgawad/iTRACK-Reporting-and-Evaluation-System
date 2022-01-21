from django.conf.urls import url

from . import views
app_name="perform"

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.performshow, name='performshow'),
    url(r'^performload$', views.performload, name='performload'),
    url(r'^performload/$', views.performload, name='performload'),
    #url(r'^performupload$', views.performupload, name='performupload'),
    #url(r'^performupload/$', views.performupload, name='performupload'),
    url(r'^performshow$', views.performshow, name='performshow'),
    url(r'^performshow/$', views.performshow, name='performshow'),
    url(r'^sopentry$', views.sopentry, name='sopentry'),
    url(r'^sopentry/$', views.sopentry, name='sopentry'),
    url(r'^sopshow$', views.sopshow, name='sopshow'),
    url(r'^sopshow/$', views.sopshow, name='sopshow'),
    url(r'^sop_show_data$', views.sop_show_data, name='sop_show_data'),
    url(r'^sop_show_data/$', views.sop_show_data, name='sop_show_data'),
    url(r'^sop_items_data$', views.sop_items_data, name='sop_items_data'),
    url(r'^sop_items_data/$', views.sop_items_data, name='sop_items_data'),
    url(r'^sop_entry_data$', views.sop_entry_data, name='sop_entry_data'),
    url(r'^sop_entry_data/$', views.sop_entry_data, name='sop_entry_data'),
    url(r'^perform_load_data$', views.perform_load_data, name='perform_load_data'),
    url(r'^perform_load_data/$', views.perform_load_data, name='perform_load_data'),
    url(r'^perform_ind_data$', views.perform_ind_data, name='perform_ind_data'),
    url(r'^perform_ind_data/$', views.perform_ind_data, name='perform_ind_data'),
]