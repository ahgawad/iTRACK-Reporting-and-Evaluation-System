from django.http import HttpResponse
#from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *
from core.models import *
import logging
from django.utils.dateparse import parse_date
#from datetime import date
from datetime import datetime
import json


#from django.contrib.auth.models import User

@login_required(login_url='/accounts/login/')
def sur_questions_data(request):
    logger = logging.getLogger(__name__)
    UserName = request.user.username;

    filter_survey = int(request.GET.get("filter_survey")) #usid_id=filter_survey
    #filter_team = request.GET.get("filter_team")# teams__team_members=filter_team
    filter_component = int(request.GET.get("filter_component"))
    filter_version = int(request.GET.get("filter_version"))

    querysetUserSurveyAnswer = UserSurveyAnswer.objects.filter( usid_id=filter_survey,
                                                                uid=request.user,
                                                                icid=filter_component,
                                                                icvid=filter_version)
    if querysetUserSurveyAnswer.exists():
        response = JsonResponse({"error": "you have filled this before"})
        response.status_code = 403  # To announce that the user isn't allowed to publish
        return response


    chartdataraw = {}
    querysetSurvey = UserSurvey.objects.filter(usid=filter_survey)[0]
    question_min_value=querysetSurvey.question_min_value
    question_max_value=querysetSurvey.question_max_value
    #NumDegrees = question_max_value + (-1 * question_min_value) + 1; # {'1':   , '2':   ,      'NumDegrees': }

    chartdataElement = {}
    querysetSurveyQuestions = UserSurveyQuestion.objects.filter(usid_id=filter_survey)
    for querysetSurveyQuestion in querysetSurveyQuestions:
        chartdataraw[querysetSurveyQuestion.usqid] = {"usqid": str(querysetSurveyQuestion.usqid),
                                                      "Question": str(querysetSurveyQuestion.question_text),
                                                      "Min_text": str(querysetSurveyQuestion.question_min_text),
                                                      "Max_text": str(querysetSurveyQuestion.question_max_text),
                                                      "Construct": str(querysetSurveyQuestion.usqcid)}

        chartdataraw[querysetSurveyQuestion.usqid].update(chartdataElement)

    logger.error('chartdata 1' +str(chartdataraw))

    response = {'chartdata':list(chartdataraw.values()),'question_min_value':question_min_value, 'question_max_value':question_max_value}
    logger.error('list(chartdataraw.values)=' + str(list(chartdataraw.values())))
    logger.error('response 1' +str(response))

    response = JsonResponse(response)
    logger.error('response 2' +str(response))

    return response #JsonResponse(queryset)




@login_required(login_url='/accounts/login/')
def sur_entry_data(request):
    logger = logging.getLogger(__name__)
    UserName = request.user.username;

    filter_survey = int(request.GET.get("filter_survey")) #usid_id=filter_survey
    #filter_team = request.GET.get("filter_team")# teams__team_members=filter_team
    filter_component = int(request.GET.get("filter_component"))
    filter_version = int(request.GET.get("filter_version"))
    questions_answers = json.loads(request.GET.get("questions_answers"))

    logger.error("questions_answers: " + str(questions_answers))

    S = UserSurvey.objects.filter(usid=filter_survey)[0]
    C = ITRACKComponent.objects.filter(icid=filter_component)[0]
    V = ITRACKComponentVersion.objects.filter(icvid=filter_version)[0]
    P = UserSurveyAnswer.objects.create(usid=S,
                                        uid=request.user,
                                        icid=C,
                                        icvid=V)
    P.save()
    for key, val in questions_answers.items():
        logger.error("key: " + str(key)+"-- val: " + str(key))
        Q = UserSurveyQuestion.objects.filter(usqid=int(key))[0]
        F = UserSurveyQuestionAnswer.objects.create(usaid=P,
                                                    usqid=Q,
                                                    answer_value=int(val))
        F.save()

    return HttpResponse("Success: " + UserName)


#@login_required
@login_required(login_url='/accounts/login/')
def sur_charts_data(request):
    logger = logging.getLogger(__name__)
    #data = request.cleaned_data["GET"]

    filter_survey = int(request.GET.get("filter_survey")) #usid_id=filter_survey
    #filter_team = request.GET.get("filter_team")# teams__team_members=filter_team
    filter_component = int(request.GET.get("filter_component"))
    filter_version = int(request.GET.get("filter_version"))

    filter_start_date = parse_date(request.GET.get("filter_start_date"))
    filter_end_date = parse_date(request.GET.get("filter_end_date"))

    filter_start_date=datetime.combine(filter_start_date, datetime.min.time())
    filter_end_date=datetime.combine(filter_end_date, datetime.min.time())


    querysetSurveyAnswers = UserSurveyAnswer.objects.filter(usid_id=filter_survey,
                                                            icid_id=filter_component,
                                                            icvid_id=filter_version,
                                                            answer_timestamp__gte=filter_start_date,
                                                            answer_timestamp__lte=filter_end_date).values_list('usaid')

    logger.error('List' +str(querysetSurveyAnswers))

    if querysetSurveyAnswers.exists():
        chartdataraw = {}
        querysetSurvey = UserSurvey.objects.filter(usid=filter_survey)[0]
        question_min_value=querysetSurvey.question_min_value
        question_max_value=querysetSurvey.question_max_value
        #NumDegrees = question_max_value + (-1 * question_min_value) + 1; # {'1':   , '2':   ,      'NumDegrees': }
        logger.error("querysetSurvey: "+str(querysetSurvey))

        chartdataElement = {}
        if question_min_value < question_max_value + 1:
            tempRange = range(1, question_max_value - question_min_value + 2)
        else:
            tempRange = range(1, question_min_value - question_max_value + 2)
        for i in tempRange:
            chartdataElement[str(i)] = 0

        logger.error("chartdataElement: "+str(chartdataElement))

        querysetSurveyQuestions = UserSurveyQuestion.objects.filter(usid_id=filter_survey)
        for index,querysetSurveyQuestion in enumerate(querysetSurveyQuestions):
            chartdataraw[querysetSurveyQuestion.usqid] = {"Question": "Q"+str(index+1),
                                                          "Question_text": str(querysetSurveyQuestion.question_text),
                                                          "Min_text": str(querysetSurveyQuestion.question_min_text),
                                                          "Max_text": str(querysetSurveyQuestion.question_max_text),
                                                          "Construct": str(querysetSurveyQuestion.usqcid)}

            chartdataraw[querysetSurveyQuestion.usqid].update(chartdataElement)

        querysetSurveyQuestionAnswers = UserSurveyQuestionAnswer.objects.filter(usaid__in=querysetSurveyAnswers).values('usqid', 'answer_value')
        logger.error('querysetSurveyQuestionAnswers: '+str(querysetSurveyQuestionAnswers))

        for querysetSurveyQuestionAnswer in querysetSurveyQuestionAnswers:
            logger.error('querysetSurveyQuestionAnswer: ' + str(querysetSurveyQuestionAnswer))
            logger.error("chartdataraw 2: " + str(chartdataraw))
            logger.error("usqid: " + str(querysetSurveyQuestionAnswer['usqid']))
            chartdataraw[querysetSurveyQuestionAnswer['usqid']][str(querysetSurveyQuestionAnswer['answer_value'])]+=1

        logger.error('OK 200')
        response = JsonResponse({'chartdata':list(chartdataraw.values()),'question_min_value':question_min_value, 'question_max_value':question_max_value})
    else:
        logger.error('error 204')

        response = JsonResponse({"error": "no data available"})
        response.status_code = 403 # 204   # To announce no content

    return response #JsonResponse(queryset)



@login_required(login_url='/accounts/login/')
def surveyshow(request):
    #UserName = request.user.username;
    #return HttpResponse("Hello, " + UserName + ". You're at the iTRACK reporting evalution development index.")
    #varval=0
    #context = {'varname': varval,}
    context = {}
    context['surveys_list'] = UserSurvey.objects.all()
    #context['teams_list'] = Team.objects.all()
    context['components_list'] = ITRACKComponent.objects.all()
    context['versions_list'] = ITRACKComponentVersion.objects.all()
    return render(request, 'surveyshow.html', context)

@login_required(login_url='/accounts/login/')
def surveyentry(request):
    #UserName = request.user.username;
    #return HttpResponse("Hello, " + UserName + ". You're at the iTRACK reporting evalution development index.")
    #varval=0
    #context = {'varname': varval,}
    context = {}
    context['surveys_list'] = UserSurvey.objects.all()
    #context['teams_list'] = Team.objects.all()
    context['components_list'] = ITRACKComponent.objects.all()
    context['versions_list'] = ITRACKComponentVersion.objects.all()
    return render(request, 'surveyentry.html', context)