from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#import json
from django.http import JsonResponse
from .models import *
from core.models import *
import logging
#from itertools import chain

#from django.contrib.auth.models import User

#@login_required
@login_required(login_url='/accounts/login/')
def dev_ind_data(request):
    logger = logging.getLogger(__name__)
    #logger.error('Request log: '+str(request))

    filter_indicator = request.GET.get("filter_indicator")
    filter_component = request.GET.get("filter_component")
    filter_version = request.GET.get("filter_version")

    querysetComponentIndicatorValue = ITRACKComponentIndicatorValue.objects.filter(iciid_id=int(filter_indicator), icid_id=int(filter_component), icvid_id=int(filter_version))
    querysetComponentIndicatorValue_filtered = querysetComponentIndicatorValue.filter()
    querysetComponentElements = ITRACKComponentElement.objects.filter( icid_id=int(filter_component))
    querysetComponentElements_filtered = querysetComponentElements.filter()
    querysetElementIndicatorValue = ITRACKComponentElementIndicatorValue.objects.filter(iciid_id=int(filter_indicator), icvid_id=int(filter_version), iceid__in=querysetComponentElements)
    querysetElementIndicatorValue_filtered = querysetElementIndicatorValue.filter()

    #querysetSelectedElementIndicatorValue=chain(querysetElementIndicatorValue , querysetComponentElements)
    #querysetSelectedElementIndicatorValue = querysetElementIndicatorValue#&querysetComponentElements
    #logger.error('queryset log: '+str(querysetSelectedElementIndicatorValue))
    #logger.error('queryset_filtered log: ' + str(querysetElementIndicatorValue))
    #queryset = ITRACKComponentIndicatorValue.objects.all()
    #response = JsonResponse(dict(response=list(querysetComponentIndicatorValue.values('icid_id', 'indicator_value'))))

    response = JsonResponse(dict(response=list(querysetElementIndicatorValue.values('iceid__itrack_component_element_name','indicator_value'))))
    #logger.error('response log: ' + str(response))
    return response #JsonResponse(queryset)



@login_required(login_url='/accounts/login/')
def index(request):
    #UserName = request.user.username;
    #return HttpResponse("Hello, " + UserName + ". You're at the iTRACK reporting evalution development index.")
    #varval=0
    #context = {'varname': varval,}
    context = {}
    context['indicators_list'] = ITRACKComponentDevelopmentIndicator.objects.all()
    context['components_list'] = ITRACKComponent.objects.all()
    context['versions_list'] = ITRACKComponentVersion.objects.all()
    return render(request, 'developshow.html', context)
