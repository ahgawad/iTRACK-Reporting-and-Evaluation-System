"""itrack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
import itrack.views
import develop.views
import survey.views
import perform.views
from . import views

urlpatterns = [
    #url(r'^admin', admin.site.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^$', itrack.views.index, name='index'),
    url(r'^docs/', itrack.views.index, name='index'),
    #url(r'^develop', include('develop.urls')),
    url(r'^develop/', include('develop.urls')),
    url(r'^dev_ind_data', develop.views.dev_ind_data, name='dev_ind_data'),
    url(r'^dev_ind_data/', develop.views.dev_ind_data, name='dev_ind_data'),
    # url(r'^charts_data', develop.views.charts_data, name='charts_data'),
    # url(r'^charts_data/', develop.views.charts_data, name='charts_data'),
    # url(r'^survey', include('survey.urls')),
    url(r'^survey/', include('survey.urls')),
    url(r'^sur_charts_data', survey.views.sur_charts_data, name='sur_charts_data'),
    url(r'^sur_charts_data/', survey.views.sur_charts_data, name='sur_charts_data'),
    url(r'^sur_entry_data', survey.views.sur_entry_data, name='sur_entry_data'),
    url(r'^sur_entry_data/', survey.views.sur_entry_data, name='sur_entry_data'),
    url(r'^sur_questions_data', survey.views.sur_questions_data, name='sur_questions_data'),
    url(r'^sur_questions_data/', survey.views.sur_questions_data, name='sur_questions_data'),
    # url(r'^perform', include('perform.urls')),
    url(r'^perform/', include('perform.urls')),
    url(r'^sop_items_data', perform.views.sop_items_data, name='sop_items_data'),
    url(r'^sop_items_data/', perform.views.sop_items_data, name='sop_items_data'),
    url(r'^sop_entry_data', perform.views.sop_entry_data, name='sop_entry_data'),
    url(r'^sop_entry_data/', perform.views.sop_entry_data, name='sop_entry_data'),
    url(r'^sop_show_data', perform.views.sop_show_data, name='sop_show_data'),
    url(r'^sop_show_data/', perform.views.sop_show_data, name='sop_show_data'),
    url(r'^perform_load_data', perform.views.perform_load_data, name='perform_load_data'),
    url(r'^perform_load_data/', perform.views.perform_load_data, name='perform_load_data'),
    url(r'^perform_ind_data', perform.views.perform_ind_data, name='perform_ind_data'),
    url(r'^perform_ind_data/', perform.views.perform_ind_data, name='perform_ind_data'),
    url(r'^accounts', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
