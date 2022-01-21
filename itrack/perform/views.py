from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from .models import *
from core.models import *
import logging
from django.http import JsonResponse
import json
#import tempfile
from django.views.decorators.csrf import csrf_exempt
#from django.utils.dateparse import parse_date
#from datetime import date
from datetime import datetime
import dateutil.parser
from itertools import chain
#from operator import attrgetter
from django.db.models import Sum, Avg
from django.db import connection
from statistics import mean

keys_sop_policies_tags={
    1:'Travel-General SOP/Policy',
    2:'Travel-Convoy SOP/Policy',
    3:'Travel-Checkpoint SOP/Policy',
    4:'Travel-landmine SOP/Policy',
    5:'Travel-Crossfire SOP/Policy',
    6:'Travel-Kidnap SOP/Policy',
    7:'Home SOP/Policy',
    8:'Office-Project site SOP/Policy',
    9:'Mob violance SOP/Policy',
    10:'First aid SOP/Policy',
    11:'Abduction SOP/Policy',
    12:'Hostage or detention SOP/Policy',
    13:'SRM General SOP/Policy',
}

keys_sop_policies_importance_levels={
    1:'Must-Have SOP/Policy',
    2:'Important SOP/Policy',
    3:'Nice-to-Have SOP/Policy',
}

keys_sop_policies_importance_levels_summerized={
    1:'Must-Have',
    2:'Important',
    3:'Nice-to-Have',
}

'''
keys_means_of_attacks={
    '*': 'Unspecified',
    'AB': 'Aerial bombardment/missile/mortar/RPG/lobbed grenade',
    'BA': 'Bodily assault/beating/stabbing with non-fire weapons or no weapons',
    'B': 'Bombing (set explosives with a stationary target: building: facility: home)',
    'BBIED': 'Body-borne IED',
    'CX': 'Complex attack (explosives in conjunction with small arms)',
    'RIED': 'Roadside IED',
    'VBIED': 'Vehicle-born IED (unknown whether remote control or suicide)',
    'VBIED-RC': 'Vehicle-borne IED (remote control detonation)',
    'VBIED-S': 'Vehicle-borne IED (suicide)',
    'K': 'Kidnapping (not killed)',
    'KK': 'Kidnap-killing',
    'RSA': 'Rape or serious sexual assault',
    'LM': 'Landmine or UXO detonation',
    'S': 'Shooting (small arms / light weapons: e.g. pistols: rifles: machine guns)',
}
'''
keys_means_of_attacks={
    '*': 'Unspecified',
    'AB': 'Aerial bombardment/missile/mortar/RPG/lobbed grenade',
    'BA': 'Bodily assault/beating/stabbing with non-fire weapons or no weapons',
    'BA-K': 'Bodily assault/beating/stabbing with non-fire weapons or no weapons -> Kidnapping (not killed)',
    'B': 'Bombing (set explosives with a stationary target: building: facility: home)',
    'BBIED': 'Body-borne IED',
    'CX': 'Complex attack (explosives in conjunction with small arms)',
    'CX-K': 'Complex attack (explosives in conjunction with small arms) -> Kidnapping (not killed)',
    'RIED': 'Roadside IED',
    'VBIED': 'Vehicle-born IED (unknown whether remote control or suicide)',
    'VBIED-RC': 'Vehicle-borne IED (remote control detonation)',
    'VBIED-S': 'Vehicle-borne IED (suicide)',
    'S-K': 'Shooting (small arms / light weapons: e.g. pistols: rifles: machine guns) -> Kidnapping (not killed)',
    'S-KK': 'Shooting (small arms / light weapons: e.g. pistols: rifles: machine guns)) -> Kidnap-killing',
    'S-RSA': 'Shooting (small arms / light weapons: e.g. pistols: rifles: machine guns) -> Rape or serious sexual assault',
    'LM': 'Landmine or UXO detonation',
    'S': 'Shooting (small arms / light weapons: e.g. pistols: rifles: machine guns)',
}
keys_means_of_attacks_fixed={
    'AB': 'Aerial bombardment/missile/mortar/RPG/lobbed grenade',
    'BA': 'Bodily assault/beating/stabbing with non-fire weapons or no weapons',
    'BA-K': 'Bodily assault/beating/stabbing with non-fire weapons or no weapons -> Kidnapping (not killed)',
    'B': 'Bombing (set explosives with a stationary target: building: facility: home)',
    'BBIED': 'Body-borne IED',
    'CX': 'Complex attack (explosives in conjunction with small arms)',
    'CX-K': 'Complex attack (explosives in conjunction with small arms) -> Kidnapping (not killed)',
    'RIED': 'Roadside IED',
    'VBIED': 'Vehicle-born IED (unknown whether remote control or suicide)',
    'VBIED-RC': 'Vehicle-borne IED (remote control detonation)',
    'VBIED-S': 'Vehicle-borne IED (suicide)',
    'S-K': 'Shooting (small arms / light weapons: e.g. pistols: rifles: machine guns) -> Kidnapping (not killed)',
    'S-KK': 'Shooting (small arms / light weapons: e.g. pistols: rifles: machine guns)) -> Kidnap-killing',
    'S-RSA': 'Shooting (small arms / light weapons: e.g. pistols: rifles: machine guns) -> Rape or serious sexual assault',
    'LM': 'Landmine or UXO detonation',
    'S': 'Shooting (small arms / light weapons: e.g. pistols: rifles: machine guns)',
}
keys_attack_contexts={
    '*': 'Unspecified',
    'Am': 'Ambush/attack on road',
    'C': 'Combat (or police operations) / Crossfire',
    'IA': 'Individual attack or assassination',
    'MV': 'Mob violence: rioting',
    'R': 'Raid (armed incursion by group on home: office: or project site)',
    'D': 'Detention (by official government forces or police: where abuse takes place)',
}
keys_attack_contexts_fixed={
    'Am': 'Ambush/attack on road',
    'C': 'Combat (or police operations) / Crossfire',
    'IA': 'Individual attack or assassination',
    'MV': 'Mob violence: rioting',
    'R': 'Raid (armed incursion by group on home: office: or project site)',
    'D': 'Detention (by official government forces or police: where abuse takes place)',
}
keys_locations={
    '*': 'Unspecified',
    'H': 'Home (private home: not compound)',
    'OC': 'Office or organization compound/residence',
    'PS': 'Project site (village: camp: distribution point: hospital: etc.)',
    'P': 'Other public location (street: market: restaurant: etc.)',
    'R': 'Road (in transit)',
    'C': 'Custody (official forces/police)',
}
keys_locations_fixed={
    'R': 'Road (in transit)',
    'H': 'Home (private home: not compound)',
    'OC': 'Office or organization compound/residence',
    'PS': 'Project site (village: camp: distribution point: hospital: etc.)',
    'P': 'Other public location (street: market: restaurant: etc.)',
    'C': 'Custody (official forces/police)',
}

keys_damage_types={
    '*': 'Unspecified',
    'KK': 'Staff killed',
    'K': 'Staff kidnapped',
    'W': 'Staff wounded',
    'RSA': 'Staff raped',
    'B': 'Damage in buildings',
    'V': 'Damage in vehicles',
    'C': 'Damage in commodities',
    'E': 'Damage in equipment',
}

keys_sop_policies_ds_levels={
    'O': 'Operational',
    'T': 'Tactical',
    'S': 'Strategic',
}

keys_sop_policies_implementation_stages={
    'P': 'Precautionary',
    'A': 'Adaptive',
}

keys_sop_cost_types={
    'O': 'Overall',
    'I': 'Individual',
}

keys_sop_policies_types={
    'S': 'SOP',
    'P': 'Policy',
}

keys_countries = {
    '*': 'Unspecified',
    'syria': 'Syrian Arab Republic',
    'iraq': 'Iraq',
    'yemen': 'Yemen',
}

keys_countries_fixed = {
    'syria': 'Syrian Arab Republic',
    'iraq': 'Iraq',
    'yemen': 'Yemen',
}

frequency_adverbs_dict = {
    1:"always",
    0.9:"usually",
    0.8:"normally",#;generally",
    0.7:"often",#;frequently",
    0.5:"sometimes",
    0.3:"occasionally",
    0.1:"seldom",
    0.05:"rarely",#";hardly ever",
    0:"never",
}
# ********************************************
# class     caselessDict
# purpose   emulate a normal Python dictionary
#           but with keys which can accept the
#           lower() method (typically strings).
#           Accesses to the dictionary are
#           case-insensitive but keys returned
#           from the dictionary are always in
#           the original case.
# ********************************************

class caselessDict:
    def __init__(self,inDict=None):
        """Constructor: takes conventional dictionary
           as input (or nothing)"""
        self.dict = {}
        if inDict != None:
            for key in inDict:
                k = key.lower()
                self.dict[k] = (key, inDict[key])
        self.keyList = self.dict.keys()
        return

    def __iter__(self):
        self.iterPosition = 0
        return(self)

    def next(self):
        if self.iterPosition >= len(self.keyList):
            raise StopIteration
        x = self.dict[self.keyList[self.iterPosition]][0]
        self.iterPosition += 1
        return x

    def __getitem__(self, key):
        k = key.lower()
        return self.dict[k][1]

    def __setitem__(self, key, value):
        k = key.lower()
        self.dict[k] = (key, value)
        self.keyList = self.dict.keys()

    def has_key(self, key):
        k = key.lower()
        return k in self.keyList

    def __len__(self):
        return len(self.dict)

    def keys(self):
        return [v[0] for v in self.dict.values()]

    def values(self):
        return [v[1] for v in self.dict.values()]

    def items(self):
        return self.dict.values()

    def get(self, key, alt):
        if self.has_key(key):
            return self.__getitem__(key)
        return alt

    def __contains__(self, item):
        return self.dict.has_key(item.lower())

    def __repr__(self):
        items = ", ".join([("%r: %r" % (k,v)) for k,v in self.items()])
        return "{%s}" % items

    def __str__(self):
        return repr(self)



# https://stackoverflow.com/questions/10048571/python-finding-a-trend-in-a-set-of-numbers
def linreg(X, Y):
    """
    return a,b in solution to y = ax + b such that root mean square distance between trend line and original points is minimized
    """
    N = len(X)
    Sx = Sy = Sxx = Syy = Sxy = 0.0
    for x, y in zip(X, Y):
        Sx = Sx + x
        Sy = Sy + y
        Sxx = Sxx + x*x
        Syy = Syy + y*y
        Sxy = Sxy + x*y
    det = Sxx * N - Sx * Sx
    return (Sxy * N - Sy * Sx)/det, (Sxx * Sy - Sx * Sxy)/det


def linreg2(X2, Y):
    """
    return a,b in solution to y = ax + b such that root mean square distance between trend line and original points is minimized
    return avg, min with time, max with time
    """

    N = len(X2)
    minX = min(X2).toordinal()
    X = [x.toordinal() - minX for x in X2]
    Sx = Sy = Sxx = Syy = Sxy = 0.0
    for x, y in zip(X, Y):
        Sx = Sx + x
        Sy = Sy + y
        Sxx = Sxx + x*x
        Syy = Syy + y*y
        Sxy = Sxy + x*y
    det = Sxx * N - Sx * Sx
    maxY = max(Y)
    minY = min(Y)
    if det != 0:
        return (Sxy * N - Sy * Sx)/det, (Sxx * Sy - Sx * Sxy)/det, mean(Y), minY, X2[Y.index(minY)], maxY, X2[Y.index(maxY)]
    else:
        # Undefined slope --> Vertical line
        return float("inf"), X[0], mean(Y), minY, X2[Y.index(minY)], maxY, X2[Y.index(maxY)]


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

#@login_required
@login_required(login_url='/accounts/login/')
def performshow(request):
    logger = logging.getLogger(__name__)
    context = {}
    #models.perform_mission_mission_leaders
    #allMissionLeadersQuerySet = Mission.mission_leaders.through.objects.all()
    #allMissionLeadersQuerySet = Mission.mission_leaders.through.objects.filter(user=request.user)

    '''
    context["keys_sop_policies_tag"] = keys_sop_policies_tags
    context["keys_location"] = keys_locations
    context["keys_attack_context"] = keys_attack_contexts
    context["keys_means_of_attack"] = keys_means_of_attacks
    context["keys_damage_type"] = keys_damage_types
    context["keys_sop_policies_ds_level"] = keys_sop_policies_ds_levels
    context["keys_sop_policies_implementation_stage"] = keys_sop_policies_implementation_stages
    context["keys_sop_cost_type"] = keys_sop_cost_types
    context["keys_sop_policies_type"] = keys_sop_policies_types
    context["keys_country"] = keys_countries
    '''

    if request.user.is_superuser:
        allTeamsQuerySet = Team.objects.all()
        if allTeamsQuerySet.exists():
            context['teams_list'] = allTeamsQuerySet
            logger.error('allTeamsQuerySet: ' + str(allTeamsQuerySet[1].team_members.all()))
            context['team_memebers_list']={}
            for oneTeamQuerySet in allTeamsQuerySet:
                context['team_memebers_list'][oneTeamQuerySet.tid]=list(oneTeamQuerySet.team_members.all().values_list('id', flat=True))
        else:
            logger.error('allTeamsQuerySet: empty ' + str(allTeamsQuerySet))
            context['teams_list'] = None

        allUsersQuerySet = User.objects.all()
        if allUsersQuerySet.exists():
            logger.error('allUsersQuerySet: ' + str(allUsersQuerySet[0]))
            context['users_list'] = allUsersQuerySet
        else:
            logger.error('allUsersQuerySet: empty' + str(allUsersQuerySet))
            context['users_list'] = None

        allMissionsQuerySet = Mission.objects.all()
        if allMissionsQuerySet.exists():
            logger.error('allMissionsQuerySet: ' + str(allMissionsQuerySet[0]))
            context['missions_list'] = allMissionsQuerySet
        else:
            logger.error('allMissionsQuerySet: empty' + str(allMissionsQuerySet))
            context['missions_list'] = None

    else:
        context['users_list'] = []
        #allTeamsQuerySet2 = Team.team_leaders.through.objects.filter(user=request.user)
        #allTeamsQuerySet = Team.objects.filter(tid__in=allTeamsQuerySet2)
        allTeamsQuerySet = Team.objects.filter(team_leaders=request.user.id)
        logger.error('allTeamsQuerySet: ' + str(allTeamsQuerySet))
        if allTeamsQuerySet.exists():
            context['teams_list'] = allTeamsQuerySet
            context['team_memebers_list']={}
            for oneTeamQuerySet in allTeamsQuerySet:
                context['users_list']=chain(context['users_list'],oneTeamQuerySet.team_members.all())
                context['team_memebers_list'][oneTeamQuerySet.tid]=list(oneTeamQuerySet.team_members.all().values_list('id', flat=True))
        else:
            logger.error('allTeamsQuerySet: empty ' + str(allTeamsQuerySet))
            context['teams_list'] = None

        logger.error('request.user.id: ' + str(request.user.id))
        allMissionsQuerySet = Mission.objects.filter(mission_leaders=request.user.id)
        logger.error('allMissionsQuerySet2: ' + str(allMissionsQuerySet))
        logger.error('allMissionsQuerySetXXX: ' + str(allMissionsQuerySet))
        if allMissionsQuerySet.exists():
            context['missions_list'] = allMissionsQuerySet
            context['mission_memebers_list']={}
            for oneMissionQuerySet in allMissionsQuerySet:
                context['users_list']=chain(context['users_list'],oneMissionQuerySet.mission_members.all())
                context['mission_memebers_list'][oneMissionQuerySet.mid]=list(oneMissionQuerySet.mission_members.all().values_list('id', flat=True))
                logger.error('context[users_list]: ' + str(context['users_list']))
        else:
            logger.error('allMissionsQuerySet: empty' + str(allMissionsQuerySet))
            context['missions_list'] = None

        if context['teams_list'] is None and context['missions_list'] is None:
            context['users_list'] = [request.user]
        else:
            context['users_list'] = list(set(context['users_list']))

    allIndicatorssQuerySet = PerformanceIndicator.objects.filter(user_related=True)
    if allIndicatorssQuerySet.exists():
        logger.error('data' + str(allIndicatorssQuerySet[0]))
        context['indicators_list'] = allIndicatorssQuerySet
    else:
        logger.error('empty' + str(allIndicatorssQuerySet))
        context['indicators_list'] = None

    allComponentsQuerySet = ITRACKComponent.objects.all()
    if allComponentsQuerySet.exists():
        context['components_list'] = allComponentsQuerySet
    else:
        context['components_list'] = None

    allTaksQuerySet = Task.objects.all()
    if allTaksQuerySet.exists():
        context['tasks_list'] = allTaksQuerySet
        logger.error('tasks_list' + str(allTaksQuerySet))
    else:
        context['components_list'] = None

    allPhasesQuerySet = Phase.objects.all()
    if allPhasesQuerySet.exists():
        context['phases_list'] = allPhasesQuerySet
        context['phase_tasks_list']={}
        logger.error('phases_list' + str(allPhasesQuerySet))
        for onePhaseQuerySet in allPhasesQuerySet:
            #I commented this during the exercise april 2019#context['tasks_list']=chain(context['tasks_list'],onePhaseQuerySet.phase_tasks.all())
            context['phase_tasks_list'][onePhaseQuerySet.pid]=list(onePhaseQuerySet.phase_tasks.all().values_list('taid', flat=True))
    else:
        context['phases_list'] = None


    #uid = request.user
    #UserSurvey.objects.filter(usid=filter_survey)
    #logger.error('tasks_list data here' + str(list(context['tasks_list'])))

    return render(request, 'performshow.html', context)

@login_required(login_url='/accounts/login/')
def performload(request):
    UserName = request.user.username;
    context = {}
    indicators_list={
        -1:'iTRACKThreatID',
        -2:'loggingComponent',
        -3:'iTRACKMissionID',
        -4:'iTRACKUserID',
        -5:'task',
        -6:'timestamp',}

    querysetPerformanceIndicators = PerformanceIndicator.objects.all()
    if querysetPerformanceIndicators.exists():
        for querysetPerformanceIndicator in querysetPerformanceIndicators:
            indicators_list[querysetPerformanceIndicator.piid] = querysetPerformanceIndicator.indicator_name
    context['indicators_list'] = indicators_list
    return render(request, 'performload.html', context)

@csrf_exempt
@login_required(login_url='/accounts/login/')
def perform_load_data(request):
    logger = logging.getLogger(__name__)
    #data = request.cleaned_data["GET"]

    fields_list = ['iTRACKThreatID','loggingComponent','iTRACKMissionID','iTRACKUserID','task','timestamp',]
    indicators_list = []
    iTRACKUserID_list = []
    loggingComponent_list = []
    iTRACKMissionID_list = []
    task_list = []
    iTRACKThreatID_list = []

    perform_ind_vals = json.loads(request.POST.get("perform_ind_vals"))
    logger.error('perform_ind_vals : ' + str(perform_ind_vals))

    UserName = request.user.username;
    for perform_ind_val in perform_ind_vals:
        for key, val in perform_ind_val.items():
            if not str(key).lower() in [str(x).lower() for x in fields_list] and not str(key).lower() in [str(x).lower() for x in indicators_list]:
                indicators_list.append(key)

            if str(key).lower() == 'itrackuserid' and val not in iTRACKUserID_list:
                logger.error('iTRACKUserID addition : ' + str(val) + ' and ' + str(val).lower())
                if str(val).lower() not in (None, '','null'):
                    iTRACKUserID_list.append(val)

            if str(key).lower() == 'loggingcomponent' and val not in loggingComponent_list:
                if str(val).lower() not in (None, '','null'):
                    loggingComponent_list.append(val)

            if str(key).lower() == 'itrackmissionid' and val not in iTRACKMissionID_list:
                if str(val).lower() not in (None, '','null'):
                    logger.error('iTRACKMissionID addition : ' + str(val) +' and ' + str(val).lower())
                    iTRACKMissionID_list.append(val)

            if str(key).lower() == 'itracktaskid' and val not in task_list:
                if str(val).lower() not in (None, '','null'):
                    logger.error('task addition : ' + str(val) +' and ' + str(val).lower())
                    task_list.append(val)

            if str(key).lower() == 'itrackthreatid' and val not in iTRACKThreatID_list:
                if str(val).lower() not in (None, '','null'):
                    iTRACKThreatID_list.append(val)

    logger.error('indicators_list : ' + str(indicators_list))
    logger.error('iTRACKUserID_list : ' + str(iTRACKUserID_list))
    logger.error('loggingComponent_list : ' + str(loggingComponent_list))
    logger.error('iTRACKMissionID_list : ' + str(iTRACKMissionID_list))
    logger.error('task_list : ' + str(task_list))
    logger.error('iTRACKThreatID_list : ' + str(iTRACKThreatID_list))

    nonExistingIndicators = []
    nonExistingiTRACKUserID = []
    nonExistingloggingComponent = []
    nonExistingiTRACKMissionID = []
    nonExistingTask = []
    nonExistingiTRACKThreatID = []

    for indicator_item in indicators_list:
        querysetPerformanceIndicator = PerformanceIndicator.objects.filter(indicator_whereabouts = indicator_item)
        if not querysetPerformanceIndicator.exists():
            nonExistingIndicators.append(indicator_item)
    if nonExistingIndicators:
        response = JsonResponse({"error": "Non-existing Indicators: " + str(nonExistingIndicators)})
        response.status_code = 406  # To announce that the user isn't allowed to publish
        return response

    for iTRACKUserID_item in iTRACKUserID_list:
        logger.error('iTRACKUserID_item : ' + str(iTRACKUserID_item))
        querysetUsers = Profile.objects.filter(itrackuid= iTRACKUserID_item)
        logger.error('querysetUsers : ' + str(querysetUsers))
        if not querysetUsers.exists():
            nonExistingiTRACKUserID.append(iTRACKUserID_item)
    if nonExistingiTRACKUserID:
        response = JsonResponse({"error": "Non-existing iTRACK User IDs: " + str(nonExistingiTRACKUserID)})
        response.status_code = 406  # To announce that the user isn't allowed to publish
        return response

    #components
    for loggingComponent_item in loggingComponent_list :
        logger.error('loggingComponent_item : ' + str(loggingComponent_item))
        querysetloggingComponents = ITRACKComponent.objects.filter(itrack_component_name=loggingComponent_item)
        logger.error('querysetloggingComponents : ' + str(querysetloggingComponents))
        if not querysetloggingComponents.exists():
            nonExistingloggingComponent.append(loggingComponent_item)
    logger.error('nonExistingloggingComponent : ' + str(nonExistingloggingComponent))
    if nonExistingloggingComponent:
        response = JsonResponse({"error": "Non-existing Logging Components: " + str(nonExistingloggingComponent)})
        response.status_code = 406  # To announce that the user isn't allowed to publish
        return response

    #mission
    for iTRACKMissionID_item in iTRACKMissionID_list:
        logger.error('iTRACKMissionID_item : ' + str(iTRACKMissionID_item))
        querysetMissions = Mission.objects.filter(itrackmid=iTRACKMissionID_item)
        logger.error('querysetMissions : ' + str(querysetMissions))
        if not querysetMissions.exists():
            nonExistingiTRACKMissionID.append(iTRACKMissionID_item)
    if nonExistingiTRACKMissionID:
        response = JsonResponse({"error": "Non-existing iTRACK Mission IDs: " + str(nonExistingiTRACKMissionID)})
        response.status_code = 406  # To announce that the user isn't allowed to publish
        return response

    #task
    for task_item in task_list:
        logger.error('task_item : ' + str(task_item))
        querysetTasks = Task.objects.filter(task_name=task_item)
        logger.error('querysetTasks : ' + str(querysetTasks))
        if not querysetTasks.exists():
            nonExistingTask.append(task_item)
    if nonExistingTask:
        response = JsonResponse({"error": "Non-existing Tasks: " + str(nonExistingTask)})
        response.status_code = 406  # To announce that the user isn't allowed to publish
        return response

    #threat
    for iTRACKThreatID_item in iTRACKThreatID_list:
        logger.error('iTRACKThreatID_item : ' + str(iTRACKThreatID_item))
        querysetThreats = Threat.objects.filter(itrackthid=iTRACKThreatID_item)
        logger.error('querysetThreats : ' + str(querysetThreats))
        if not querysetThreats.exists():
            nonExistingiTRACKThreatID.append(iTRACKThreatID_item)
    if nonExistingiTRACKThreatID:
        response = JsonResponse({"error": "Non-existing iTRACK Threat IDs: " + str(nonExistingiTRACKThreatID)})
        response.status_code = 406  # To announce that the user isn't allowed to publish
        return response

    errorResponse = ''
    for perform_ind_valO in perform_ind_vals:
        perform_ind_val = caselessDict(perform_ind_valO)
        '''
        perform_ind_val = {}
        for key in perform_ind_valO:
            k = key.lower()
            perform_ind_val[k] = (key, perform_ind_valO[key])
        '''
        for indicators_item in indicators_list:
            querysetPerformanceIndicator = PerformanceIndicator.objects.filter(indicator_whereabouts = indicators_item)
            querysetUsers = Profile.objects.filter(itrackuid = perform_ind_val.get('iTRACKUserID', 'Null'))
            querysetloggingComponents = ITRACKComponent.objects.filter(itrack_component_name = perform_ind_val.get('loggingComponent', 'Null'))
            querysetMissions = Mission.objects.filter(itrackmid = perform_ind_val.get('iTRACKMissionID', 'Null'))

            querysetThreats = Threat.objects.filter(itrackthid=perform_ind_val.get('iTRACKThreatID', 'Null'))
            querysetTasks = Task.objects.filter(task_name = perform_ind_val.get('task', 'Null'))

            if querysetPerformanceIndicator.exists() and querysetUsers.exists() and querysetloggingComponents.exists() and querysetMissions.exists():
                if querysetThreats.exists(): querysetThreats_item = querysetThreats[0]
                else: querysetThreats_item = None
                if querysetTasks.exists(): querysetTasks_item = querysetTasks[0]
                else: querysetTasks_item = None
                T = PerformanceIndicatorValue.objects.filter(piid=querysetPerformanceIndicator[0],
                                                             uid=querysetUsers[0].user,
                                                             icid=querysetloggingComponents[0],
                                                             mid=querysetMissions[0],
                                                             thid=querysetThreats_item,
                                                             taid=querysetTasks_item,
                                                             indicator_value_log_timestamp=dateutil.parser.parse(
                                                                 perform_ind_val['timestamp']),
                                                             indicator_value=perform_ind_val[indicators_item])
                if not T.exists():
                    V = PerformanceIndicatorValue.objects.create(piid=querysetPerformanceIndicator[0],
                                                                 uid=querysetUsers[0].user,
                                                                 icid=querysetloggingComponents[0],
                                                                 mid=querysetMissions[0],
                                                                 thid=querysetThreats_item,
                                                                 taid=querysetTasks_item,
                                                                 indicator_value_log_timestamp=dateutil.parser.parse(
                                                                     perform_ind_val['timestamp']),
                                                                 indicator_value=perform_ind_val[indicators_item])
                    V.save()
                else:
                    pass
                    #response = JsonResponse({"error": "Some of the records have been uploaded before!"})
                    #response.status_code = 406  # To announce that the user isn't allowed to publish
                    #return response
            else:
                errorResponse += str(perform_ind_val) + "\r\n"
                #querysetPerformanceIndicator.exists()
                #querysetUsers.exists()
                #querysetloggingComponents.exists()
                #querysetMissions.exists()

    if errorResponse:
        response = JsonResponse(
            {"error": "Not-enough information to save indicators in the following objects: \r\n" + errorResponse})
        response.status_code = 406  # To announce that the user isn't allowed to publish
        return response

    return HttpResponse("Success: " + UserName)


@login_required(login_url='/accounts/login/')
def performupload(request):
    logger = logging.getLogger(__name__)
    UserName = request.user.username;
    context = {}
    if request.method == 'POST':
        '''
        # Creates a file and returns a tuple containing both the handle and the path.
        handle, path = tempfile.mkstemp()
        with open(handle, 'wb+') as destination:
            for chunk in request.FILES['file-selector'].chunks():
                destination.write(chunk)
        logger.error('file handel: ' + str(handle)+' and filename: '+path)
        str_text = ''
        
        for line in handle:
            str_text = str_text + line.decode("utf-8") 
        jsonData = json.loads(str_text)  # converts to a json structure
        logger.error('json1 : ' + str(jsonData))
        '''

        uploaded_file = request.FILES['file-selector']
        str_text = ''
        for line in uploaded_file:
            str_text = str_text + line.decode("utf-8").rstrip('\n').rstrip('\r')

        #if str_text.find(',]'):
        #    str_text.replace(',]', ']')

        if str_text[-2:] == ',]':
            str_text = str_text[:-2]+']'

        logger.error('str text : ' + str_text)
        jsonData = json.loads(str_text)  # converts to a json structure
        logger.error('json2 : ' + str(jsonData))
        context['jsonData']=jsonData


        return render(request, 'performuploaded.html', context)

    return render(request, 'performupload.html', context)


@login_required(login_url='/accounts/login/')
def sopentry(request):
    logger = logging.getLogger(__name__)
    context = {}
    #models.perform_mission_mission_leaders
    #allMissionLeadersQuerySet = Mission.mission_leaders.through.objects.all()
    #allMissionLeadersQuerySet = Mission.mission_leaders.through.objects.filter(user=request.user)

    context["keys_sop_policies_tag"] = keys_sop_policies_tags
    context["keys_location"] = keys_locations_fixed
    context["keys_attack_context"] = keys_attack_contexts_fixed
    context["keys_means_of_attack"] = keys_means_of_attacks_fixed
    context["keys_damage_type"] = keys_damage_types
    context["keys_sop_policies_ds_level"] = keys_sop_policies_ds_levels
    context["keys_sop_policies_implementation_stage"] = keys_sop_policies_implementation_stages
    context["keys_sop_cost_type"] = keys_sop_cost_types
    context["keys_sop_policies_type"] = keys_sop_policies_types
    context["keys_country"] = keys_countries_fixed

    allMissionLeadersQuerySet = Mission.objects.filter(mission_leaders=request.user)
    if allMissionLeadersQuerySet.exists():
        logger.error('data' + str(allMissionLeadersQuerySet[0]))
        context['missions_list'] = allMissionLeadersQuerySet
    else:
        logger.error('empty' + str(allMissionLeadersQuerySet))
        context['missions_list'] = None

        #uid = request.user
    #UserSurvey.objects.filter(usid=filter_survey)

    return render(request, 'sopentry.html', context)

@login_required(login_url='/accounts/login/')
def sopshow(request):
    logger = logging.getLogger(__name__)
    context = {}
    #models.perform_mission_mission_leaders
    #allMissionLeadersQuerySet = Mission.mission_leaders.through.objects.all()
    #allMissionLeadersQuerySet = Mission.mission_leaders.through.objects.filter(user=request.user)

    context["keys_sop_policies_tag"] = keys_sop_policies_tags
    context["keys_location"] = keys_locations
    context["keys_attack_context"] = keys_attack_contexts
    context["keys_means_of_attack"] = keys_means_of_attacks
    context["keys_damage_type"] = keys_damage_types
    context["keys_sop_policies_ds_level"] = keys_sop_policies_ds_levels
    context["keys_sop_policies_implementation_stage"] = keys_sop_policies_implementation_stages
    context["keys_sop_cost_type"] = keys_sop_cost_types
    context["keys_sop_policies_type"] = keys_sop_policies_types
    context["keys_country"] = keys_countries

    allMissionLeadersQuerySet = Mission.objects.filter(mission_leaders=request.user)
    if allMissionLeadersQuerySet.exists():
        logger.error('data' + str(allMissionLeadersQuerySet[0]))
        context['missions_list'] = allMissionLeadersQuerySet
    else:
        logger.error('empty' + str(allMissionLeadersQuerySet))
        context['missions_list'] = None

        #uid = request.user
    #UserSurvey.objects.filter(usid=filter_survey)
    return render(request, 'sopshow.html', context)


@login_required(login_url='/accounts/login/')
def sop_show_data(request):
    UserName = request.user.username;
    logger = logging.getLogger(__name__)
    filter_missions = [int(s) for s in str(request.GET.get("filter_missions")).split(',')]
    #filter_country = request.GET.get("filter_country")
    filter_country = '*'
    #filter_location = request.GET.get("filter_location")
    filter_location = '*'
    #filter_attack_context = request.GET.get("filter_attack_context")
    filter_attack_context = '*'
    #filter_means_of_attack = request.GET.get("filter_means_of_attack")
    filter_means_of_attack = '*'

    #keys_sop_policies_importance_levels

    # SWM: Must-Have SOP/Policy Weight
    # SWI: Important SOP/Policy Weight
    # SWN: Nice-to-Have SOP/Policy Weight
    SWM = Setting.objects.get(setting_name='SWM').setting_value
    SWI = Setting.objects.get(setting_name='SWI').setting_value
    SWN = Setting.objects.get(setting_name='SWN').setting_value

    sop_importance_weights = {1:SWM,2:SWI,3:SWN}

    '''
    sopsPoliciesSurveyAnswerList = list(Sop_policySurveyAnswer.objects.filter(mid__in=filter_missions,
                                                     Location=filter_location,
                                                     Attack_context=filter_attack_context,
                                                     Means_of_attack=filter_means_of_attack,
                                                     Country=filter_country).values_list('spsaid', flat=True))
    '''
    logger.error('List:' + str(filter_location+filter_attack_context+filter_means_of_attack+filter_country))
    if filter_country == '*':
        filter_country1 = '%'
    else:
        filter_country1 = filter_country
    if filter_location == '*':
        filter_location1 = '%'
    else:
        filter_location1 = filter_location
    if filter_attack_context == '*':
        filter_attack_context1 = '%'
    else:
        filter_attack_context1 = filter_attack_context
    if filter_means_of_attack == '*':
        filter_means_of_attack1 = '%'
    else:
        filter_means_of_attack1 = filter_means_of_attack

    SELECTSTR = "SELECT `perform_sop_policysurveyanswer`.`spsaid` FROM `perform_sop_policysurveyanswer` WHERE (`perform_sop_policysurveyanswer`.`mid_id` IN (%s) AND `perform_sop_policysurveyanswer`.`Location` LIKE '%s' AND `perform_sop_policysurveyanswer`.`Attack_context` LIKE '%s' AND `perform_sop_policysurveyanswer`.`Means_of_attack` LIKE '%s' AND `perform_sop_policysurveyanswer`.`Country` LIKE '%s');"
    with connection.cursor() as c:
        c.execute(SELECTSTR %(str(filter_missions)[1:-1], filter_location1, filter_attack_context1, filter_means_of_attack1, filter_country1))
        incidentsList = [i[0] for i in c]

    logger.error('querysetSopsPoliciesSurveyAnswer List:' + str(incidentsList))
    if len(incidentsList) < 1:
        response = JsonResponse({"error": "No data"})
        response.status_code = 400
        return response

    #querysetSopsPolicies = Sop_policy.objects.values('spid','Tag','Importance')

    #logger.error('querysetSopsPolicies List:' + str(querysetSopsPolicies[0]))

    #SELECTSTR = "SELECT `spsaid_id`,`Tag`,`Importance`,`spsqaid`,`spid`,sum(`answer_value`) FROM `perform_sop_policysurveyquestionanswer`, `perform_sop_policy` WHERE (`spsaid_id` IN (%s) AND `perform_sop_policysurveyquestionanswer`.`spid_id` = `perform_sop_policy`.`spid`) group by `spsaid_id`,`Tag`,`Importance`;"

    #querysetSop_policySurveyQuestionAnswersRAW = Sop_policySurveyQuestionAnswer.objects.raw(SELECTSTR %(str(sopsPoliciesSurveyAnswerList)[1:-1]))

    logger.error('sopsPoliciesSurveyAnswerList  XXX 1:' + str(incidentsList)[1:-1])

    #SELECTSTR = "SELECT `spsaid_id`,`Tag`,`Importance`,`spsqaid`,`spid`,sum(`answer_value`) AS sum_answer_values FROM `perform_sop_policysurveyquestionanswer`, `perform_sop_policy` WHERE (`spsaid_id` IN ( %s ) AND `perform_sop_policysurveyquestionanswer`.`spid_id` = `perform_sop_policy`.`spid`) group by `spsaid_id`,`Tag`,`Importance`;"
    SELECTSTR = "SELECT `spsaid_id` as `spsaid`,`Tag`,`Importance`,sum(`answer_value`) AS sum_answer_values FROM `perform_sop_policysurveyquestionanswer`, `perform_sop_policy` WHERE (`spsaid_id` IN ( %s ) AND `perform_sop_policysurveyquestionanswer`.`spid_id` = `perform_sop_policy`.`spid`) group by `spsaid_id`,`Tag`,`Importance`;"
    with connection.cursor() as c:
        c.execute(SELECTSTR %(str(incidentsList)[1:-1]))
        sumAnswerValuesList = dictfetchall(c)
        ## {'spsaid': 1, 'Tag': 1, 'Importance': 2, 'sum_answer_values': Decimal('18')}
    logger.error('sumAnswerValuesList  (NUM):' + str(len(sumAnswerValuesList)))
    logger.error('sumAnswerValuesList  (NUM):' + str(list(sumAnswerValuesList)))

    SELECTSTR = "SELECT `mission_name`,`spsaid`,`mission_end_date` FROM `perform_sop_policysurveyanswer`,`core_mission` WHERE `perform_sop_policysurveyanswer`.`mid_id` = `core_mission`.`mid`;"
    with connection.cursor() as c:
        c.execute(SELECTSTR)# %(filter_country1,filter_location1,filter_attack_context1,filter_means_of_attack1 ))
        #%(filter_indicator, str(filter_users)[1:-1], str(filter_missions)[1:-1], str(filter_tasks)[1:-1],filter_start_date, filter_end_date)
        missionInfoList = dictfetchall(c)
        ## {'spsaid': 15, 'mission_end_date': datetime.datetime(2018, 5, 5, 17, 0)}
    logger.error('missionInfoList (DATE):' + str(list(missionInfoList)))

    '''
    countSopsList = []
    # SELECTSTR = "SELECT `Tag`,`Importance`,count(*) AS count_sops FROM `perform_sop_policy` group by `Tag`,`Importance`;"
    for missionInfoItem in missionInfoList:
        SELECTSTR = "SELECT `Country` AS 'filter_countryItem', `Location` AS 'filter_locationItem', `Attack_context` AS 'filter_attack_contextItem', `Means_of_attack` AS 'filter_means_of_attackItem' FROM `perform_sop_policysurveyanswer` WHERE `spsaid` = %s;"
        with connection.cursor() as c:
            c.execute(SELECTSTR %(missionInfoItem['spsaid']))
            countSopsItem = dictfetchall(c)

        logger.error('countSopsItem YYY:' + str(countSopsItem))

        if countSopsItem[0]['filter_countryItem'] == '*':
            filter_country2 = '%'
        else:
            filter_country2 = countSopsItem[0]['filter_countryItem']
        if countSopsItem[0]['filter_locationItem'] == '*':
            filter_location2 = '%'
        else:
            filter_location2 = countSopsItem[0]['filter_locationItem']
        if countSopsItem[0]['filter_attack_contextItem'] == '*':
            filter_attack_context2 = '%'
        else:
            filter_attack_context2 = countSopsItem[0]['filter_attack_contextItem']
        if countSopsItem[0]['filter_means_of_attackItem'] == '*':
            filter_means_of_attack2 = '%'
        else:
            filter_means_of_attack2 = countSopsItem[0]['filter_means_of_attackItem']

        SELECTSTR = "SELECT `Tag`,`Importance`,count(*) AS count_sops FROM `perform_sop_policy` WHERE (`Country` like '%s' AND `Location` like '%s' AND `Attack_context` like '%s' AND `Means_of_attack` like '%s') group by `Tag`,`Importance`;"
        with connection.cursor() as c:
            c.execute(SELECTSTR %(filter_country2,filter_location2,filter_attack_context2,filter_means_of_attack2))
            #%(filter_indicator, str(filter_users)[1:-1], str(filter_missions)[1:-1], str(filter_tasks)[1:-1],filter_start_date, filter_end_date)
            countSopsList.append(dictfetchall(c))
            #{'Tag': 9, 'Importance': 2, 'count_sops': 58}
        logger.error('querysetSop_policyRAWList XXX:' + str(countSopsList))
    logger.error('querysetSop_policyRAWList XXX:' + str(countSopsList))
    '''

    SELECTSTR = "SELECT `Tag`,`Importance`,count(*) AS count_sops FROM `perform_sop_policy` WHERE (`Country` like '%s' AND `Location` like '%s' AND `Attack_context` like '%s' AND `Means_of_attack` like '%s') group by `Tag`,`Importance`;"
    with connection.cursor() as c:
        c.execute(SELECTSTR % (filter_country1, filter_location1, filter_attack_context1, filter_means_of_attack1))
        # %(filter_indicator, str(filter_users)[1:-1], str(filter_missions)[1:-1], str(filter_tasks)[1:-1],filter_start_date, filter_end_date)
        countSopsList=dictfetchall(c)
        ## {'Tag': 9, 'Importance': 2, 'count_sops': 58}

    logger.error('countSopsList (DEN):' + str(countSopsList))

    soppol_x = {}
    soppol_y = {}

    sop_indicator_values_objects_by_tag = {}
    for keys_sop_policies_tag in keys_sop_policies_tags:
        sop_indicator_values_objects = {}
        soppol_x[keys_sop_policies_tag] = []
        soppol_y[keys_sop_policies_tag] = []
        for sumAnswerValuesItem in sumAnswerValuesList:
            #logger.error("sumAnswerValuesItem['spsaid']:" + str(sumAnswerValuesItem['spsaid']))
            #sumAnswerValuesItem['sum_answer_values']

            if  sumAnswerValuesItem['Tag']==keys_sop_policies_tag:
                '''
                sop_indicator_values_objects[sumAnswerValuesItem['spsaid']] = {
                        'x': next((missionInfoItem['mission_end_date'] for missionInfoItem in missionInfoList if missionInfoItem['spsaid'] == sumAnswerValuesItem['spsaid']), datetime.now()).strftime("%Y-%m-%d %H:%M"),
                        'y': sumAnswerValuesItem['sum_answer_values'] * sop_importance_weights[sumAnswerValuesItem['Importance']]}
                '''
                missionInfoItemMissionName = next((missionInfoItem['mission_name'] for missionInfoItem in missionInfoList if
                      missionInfoItem['spsaid'] == sumAnswerValuesItem['spsaid']), "Unknown mission")

                missionInfoItemMissionEndDate = next((missionInfoItem['mission_end_date'] for missionInfoItem in missionInfoList if
                      missionInfoItem['spsaid'] == sumAnswerValuesItem['spsaid']), datetime.now()).strftime("%Y-%m-%d %H:%M")

                missionInfoItemMissionEndDateOrg = next((missionInfoItem['mission_end_date'] for missionInfoItem in missionInfoList if
                      missionInfoItem['spsaid'] == sumAnswerValuesItem['spsaid']), datetime.now())

                soppol_x[keys_sop_policies_tag].append(missionInfoItemMissionEndDateOrg)
                soppol_y[keys_sop_policies_tag].append(float(sumAnswerValuesItem['sum_answer_values'])*sop_importance_weights[sumAnswerValuesItem['Importance']])

                if missionInfoItemMissionName in sop_indicator_values_objects:
                    sop_indicator_values_objects[missionInfoItemMissionName].append(
                        {'x': missionInfoItemMissionEndDate,
                         'y': float(sumAnswerValuesItem['sum_answer_values'])*sop_importance_weights[sumAnswerValuesItem['Importance']]})
                else:
                    sop_indicator_values_objects[missionInfoItemMissionName] = [
                        {'x': missionInfoItemMissionEndDate,
                         'y': float(sumAnswerValuesItem['sum_answer_values'])*sop_importance_weights[sumAnswerValuesItem['Importance']]}]

        logger.error('soppol_x :' + str(soppol_x[1]))
        logger.error('soppol_y :' + str(soppol_y[1]))
        sop_indicator_values_list = []
        for key, val in sop_indicator_values_objects.items():
            sop_indicator_values_list.append({'name': key, 'data': val})
        sop_indicator_values_objects_by_tag[keys_sop_policies_tag] = sop_indicator_values_list

        data = {}
        data['sop_ind_vals']=sop_indicator_values_objects_by_tag

    #logger.error('sop_indicator_values_objects_by_tag :' + str(sop_indicator_values_objects_by_tag))


    #SELECTSTR = "SELECT `Tag`,`Importance`,`spid`,IFNULL(SUM(`answer_value`),0) AS `answer_value_sum` FROM `perform_sop_policy` LEFT JOIN (SELECT * FROM `perform_sop_policysurveyquestionanswer` WHERE `spsaid_id` IN (%s)) AS `perform_sop_policysurveyquestionanswer` ON `perform_sop_policy`.`spid` = `perform_sop_policysurveyquestionanswer`.`spid_id` GROUP BY `spid`;"
    #SELECTSTR = "SELECT `Tag`,`Importance`,`spid`,IFNULL(SUM(`answer_value`),0) AS `answer_value_sum` FROM `perform_sop_policy` LEFT JOIN (SELECT * FROM `perform_sop_policysurveyquestionanswer` WHERE `spsaid_id` IN (%s)) AS `perform_sop_policysurveyquestionanswer` ON `perform_sop_policy`.`spid` = `perform_sop_policysurveyquestionanswer`.`spid_id` GROUP BY `spid` ORDER BY `Tag`,`Importance` ASC, `answer_value_sum` DESC;"
    #SELECTSTR = "SELECT `Tag`,`Importance`,`Measure_description`,IFNULL(SUM(`answer_value`),0) AS `answer_value_sum` FROM `perform_sop_policy` LEFT JOIN (SELECT * FROM `perform_sop_policysurveyquestionanswer` WHERE `spsaid_id` IN (%s)) AS `perform_sop_policysurveyquestionanswer` ON `perform_sop_policy`.`spid` = `perform_sop_policysurveyquestionanswer`.`spid_id` GROUP BY `spid` ORDER BY `Tag`,`Importance` ASC, `answer_value_sum` DESC;"
    #with connection.cursor() as c:
    #    c.execute(SELECTSTR %(str(incidentsList)[1:-1]))
    #    sumAnswerValuesPerSOPList = dictfetchall(c)
    #logger.error('sumAnswerValuesPerSOPList :' + str(sumAnswerValuesPerSOPList))


    #SELECTSTR = "SELECT `Measure_description`,IFNULL(SUM(`answer_value`),0) AS `answer_value_sum` FROM `perform_sop_policy` LEFT JOIN (SELECT * FROM `perform_sop_policysurveyquestionanswer` WHERE `spsaid_id` IN (%s)) AS `perform_sop_policysurveyquestionanswer` ON `perform_sop_policy`.`spid` = `perform_sop_policysurveyquestionanswer`.`spid_id` WHERE `Tag`=%s AND `Importance`=%s GROUP BY `spid` ORDER BY `Tag`,`Importance` ASC, `answer_value_sum` DESC;"
    #SELECTSTR = "SELECT `Measure_description`,IFNULL(SUM(`answer_value`),0) AS `answer_value_sum` FROM `perform_sop_policy` LEFT JOIN (SELECT * FROM `perform_sop_policysurveyquestionanswer` WHERE `spsaid_id` IN (%s)) AS `perform_sop_policysurveyquestionanswer` ON `perform_sop_policy`.`spid` = `perform_sop_policysurveyquestionanswer`.`spid_id` WHERE `Tag`=%s GROUP BY `spid` ORDER BY `Importance` ASC, `answer_value_sum` DESC;"
    SELECTSTR = "SELECT `Measure_description`,IFNULL(SUM(`answer_value`),0) AS `answer_value_sum` FROM `perform_sop_policy` LEFT JOIN (SELECT * FROM `perform_sop_policysurveyquestionanswer` WHERE `spsaid_id` IN (%s)) AS `perform_sop_policysurveyquestionanswer` ON `perform_sop_policy`.`spid` = `perform_sop_policysurveyquestionanswer`.`spid_id` WHERE `Tag`=%s GROUP BY `spid` ORDER BY `Importance` ASC, `answer_value_sum` ASC;"
    SELECTSTR = "SELECT `Importance`,`Measure_description`,IFNULL(SUM(`answer_value`),0)/%s AS `answer_value_frac` FROM `perform_sop_policy` LEFT JOIN (SELECT * FROM `perform_sop_policysurveyquestionanswer` WHERE `spsaid_id` IN (%s)) AS `perform_sop_policysurveyquestionanswer` ON `perform_sop_policy`.`spid` = `perform_sop_policysurveyquestionanswer`.`spid_id` WHERE `Tag`=%s GROUP BY `spid` ORDER BY `Importance` ASC, `answer_value_frac` ASC;"
    sop_executed_sorted ={}
    for keys_sop_policies_tag,values_sop_policies_tag in keys_sop_policies_tags.items():
        #for keys_sop_policies_importance_level in keys_sop_policies_importance_levels:
        with connection.cursor() as c:
            #c.execute(SELECTSTR %(str(incidentsList)[1:-1], str(keys_sop_policies_tag), str(keys_sop_policies_importance_level)))
            c.execute(SELECTSTR %(str(len(incidentsList)),str(incidentsList)[1:-1], str(keys_sop_policies_tag)))
            temp_list = dictfetchall(c)
            #frequency_adverbs_dict
            '''
            1:"always",
            0.9:"usually",
            0.8:"normally",#;generally",
            0.7:"often",#;frequently",
            0.5:"sometimes",
            0.3:"occasionally",
            0.1:"seldom",
            0.05:"rarely",#";hardly ever",
            0:"never",
            '''
            temp_list_grp={}
            temp_list_grp_len = {}
            #temp_list_grp["always"]=''
            #temp_list_grp["usually"]=''
            #temp_list_grp["normally"]=''
            #temp_list_grp["often"]=''
            #temp_list_grp["sometimes"]=''
            temp_list_grp["occasionally"]=''
            temp_list_grp["seldom"]=''
            temp_list_grp["rarely"]=''
            temp_list_grp["never"]=''

            temp_list_grp_len["occasionally"]=0
            temp_list_grp_len["seldom"]=0
            temp_list_grp_len["rarely"]=0
            temp_list_grp_len["never"]=0
            #keys_sop_policies_importance_levels_summerized
            #temp.answer_value_sum
            #temp_len = len(temp_list)

            sop_executed_sorted[keys_sop_policies_tag] = '<h6>'+values_sop_policies_tag+':</h6>'

            for temp_item in temp_list:
                #for frequency_adverbs_key,frequency_adverbs_val in frequency_adverbs_dict.items():
                #    if temp_item['answer_value_frac']<=frequency_adverbs_key:
                #        temp_list_grp[frequency_adverbs_val]+= '<il>'+ temp_item['Measure_description'] + ', with importance level: ' + keys_sop_policies_importance_levels_summerized[temp_item['Importance']] + '</il>'

                if temp_item['answer_value_frac'] == 0:
                    temp_list_grp_len['never']+= 1
                    temp_list_grp['never']+= '<li>'+ temp_item['Measure_description'] + ' [<b>' + keys_sop_policies_importance_levels_summerized[temp_item['Importance']] + '</b>]</li>'
                elif temp_item['answer_value_frac'] <= 0.05:
                    temp_list_grp_len['rarely'] += 1
                    temp_list_grp['rarely']+= '<li>'+ temp_item['Measure_description'] + ' [<b>' + keys_sop_policies_importance_levels_summerized[temp_item['Importance']] + '</b>]</li>'
                elif temp_item['answer_value_frac'] <= 0.1:
                    temp_list_grp_len['seldom'] += 1
                    temp_list_grp['seldom'] += '<li>' + temp_item['Measure_description'] + ' [<b>' + keys_sop_policies_importance_levels_summerized[temp_item['Importance']] + '</b>]</li>'
                elif temp_item['answer_value_frac'] <= 0.3:
                    temp_list_grp_len['occasionally'] += 1
                    temp_list_grp['occasionally'] += '<li>' + temp_item['Measure_description'] + ' [<b>' + keys_sop_policies_importance_levels_summerized[temp_item['Importance']] + '</b>]</li>'

            temp_prt = ''
            for key in temp_list_grp_len:
                if temp_list_grp_len[key] == 1: temp_prt += "<p>The following SOP/policy has "+str(key)+" been exeucted:</p><ul>"+temp_list_grp[key]+"</ul>"
                elif temp_list_grp_len[key] > 0: temp_prt += "<p>The following SOPs/policies have " + str(key) + " been exeucted:</p><ul>" + temp_list_grp[key] + "</ul>"

            if len(soppol_x[keys_sop_policies_tag]) > 1:
                slope, intercept, avgY, minY, minYTime, maxY, maxYTime = linreg2(soppol_x[keys_sop_policies_tag], soppol_y[keys_sop_policies_tag])

                sop_executed_sorted[keys_sop_policies_tag] += "<p>Your worst SOPs/Policies sub-indicator value is " + str(
                    round(minY, 1)) + " dated " + minYTime.strftime("%H:%m %p %A, %B %d, %Y") + ". "
                sop_executed_sorted[keys_sop_policies_tag] += "While your best SOPs/Policies sub-indicator value is " + str(
                    round(maxY, 1)) + " dated " + maxYTime.strftime("%H:%m %p %A, %B %d, %Y") + ".</p>"
                sop_executed_sorted[keys_sop_policies_tag] += "<p>Your average SOPs/Policies sub-indicator value is " + str(
                    round(avgY, 1)) + "."
                if slope != float("inf"):
                    if (slope > 0):
                        sop_executed_sorted[
                            keys_sop_policies_tag] += "<p>When it comes to performance over time, as shown in the figure, your SOPs/Policies sub-indicator performance is enhancing.</p>"
                    elif slope == 0:
                        sop_executed_sorted[
                            keys_sop_policies_tag] += "<p>When it comes to performance over time, as shown in the figure, your SOPs/Policies sub-indicator performance is neither enhancing nor deteriorating.</p>"
                    else:
                        sop_executed_sorted[
                            keys_sop_policies_tag] += "<p>When it comes to performance over time, as shown in the figure, your SOPs/Policies sub-indicator performance is deteriorating.</p>"
            elif len(soppol_x[keys_sop_policies_tag]) == 1:
                # only 1 point
                sop_executed_sorted[keys_sop_policies_tag] += "<p>Your SOPs/Policies sub-indicator value is " + str(round(soppol_y[keys_sop_policies_tag][0], 1)) + ".</p>"
            elif len(soppol_x[keys_sop_policies_tag]) == 0:
                # only 0 point
                sop_executed_sorted[keys_sop_policies_tag] += "<p>You have not executed any of the SOPs/Policies in relation to this sub-indicator.</p>"


            sop_executed_sorted[keys_sop_policies_tag] += temp_prt



    #logger.error('sop_executed_sorted :' + str(sop_executed_sorted))
    #'Yes' if fruit == 'Apple' else 'No'

    querySetMissions = Mission.objects.filter(mid__in=filter_missions)

    data['general_comment'] = "Concerning SOPs/policies, during the selected "
    if len(filter_missions) == 1:
        data['general_comment'] += "mission: "+querySetMissions[0].mission_name + ".</p>"
    else:
        data['general_comment'] += "missions:" + "</p><ul>"
        for querySetMission in querySetMissions:
            data['general_comment'] += "<li>" + querySetMission.mission_name + "</li>"
        data['general_comment'] += "</ul>" + "</p>"



    data['sop_ind_txt'] = sop_executed_sorted
    response = JsonResponse(data, safe=False)
    response.status_code = 201
    return response


@login_required(login_url='/accounts/login/')
def perform_ind_data(request):
    logger = logging.getLogger(__name__)
    #data = request.cleaned_data["GET"]

    logger.error('filter_users : ' + str([int(s) for s in str(request.GET.get("filter_users")).split(',')]))

    filter_users = [int(s) for s in str(request.GET.get("filter_users")).split(',')]

    #filter_team = request.GET.get("filter_team")# teams__team_members=filter_team
    filter_indicator = int(request.GET.get("filter_indicator"))
    filter_missions = [int(s) for s in str(request.GET.get("filter_missions")).split(',')]
    logger.error('filter_missions1 :'+ str(filter_missions))
    #filter_component = int(request.GET.get("filter_component"))
    filter_tasks = [int(s) for s in str(request.GET.get("filter_tasks")).split(',')]
    logger.error('filter_tasks1 :' + str(filter_tasks))
    #filter_start_date = parse_date(request.GET.get("filter_start_date"))
    #filter_end_date = parse_date(request.GET.get("filter_end_date"))

    #filter_start_date=datetime.combine(filter_start_date, datetime.min.time())
    #filter_end_date=datetime.combine(filter_end_date, datetime.min.time())

    #querysetPerformanceIndicator = PerformanceIndicator.objects.get(piid = filter_indicator).is_average
    #logger.error('querysetPerformanceIndicator is_average:' + str(querysetPerformanceIndicator))

    '''
    querysetPerformanceIndicatorValues = PerformanceIndicatorValue.objects.filter(piid=filter_indicator,
                                                                                  uid__in=filter_users,
                                                                                  # icid = filter_component,
                                                                                  mid__in=filter_missions,
                                                                                  taid__in=filter_tasks,
                                                                                  indicator_value_log_timestamp__gte=filter_start_date,
                                                                                  indicator_value_log_timestamp__lte=filter_end_date)
    if not querysetPerformanceIndicatorValues.exists():
        response = JsonResponse({"error": "No data"})
        response.status_code = 400
        return response
    '''
    querysetPerformanceIndicator = PerformanceIndicator.objects.get(piid = filter_indicator)
    if querysetPerformanceIndicator.is_average:
        # correct avg:
        #SELECTSTR = "SELECT `pivid`, `piid_id`, `icid_id`, `mid_id`, `thid_id`, `taid_id`, `uid_id`, avg(`indicator_value`), max(`indicator_value_log_timestamp`) FROM `perform_performanceindicatorvalue` WHERE (`piid_id` = %s AND `uid_id` IN (%s) AND  `mid_id` IN (%s) AND `taid_id` IN (%s) AND `indicator_value_log_timestamp` >= '%s' AND `indicator_value_log_timestamp` <= '%s') group by `uid_id`,`mid_id`;"
        SELECTSTR = "SELECT `pivid`, `piid_id`, `icid_id`, `mid_id`, `thid_id`, `taid_id`, `uid_id`, avg(`indicator_value`) AS `indicator_value`, max(`indicator_value_log_timestamp`) AS `indicator_value_log_timestamp` FROM `perform_performanceindicatorvalue` WHERE (`piid_id` = %s AND `uid_id` IN (%s) AND  `mid_id` IN (%s) AND `taid_id` IN (%s)) group by `uid_id`,`mid_id`;"
        querySetPerformanceIndicatorTaskTarget = PerformanceIndicatorTaskTarget.objects.filter(piid=filter_indicator,taid__in=filter_tasks).aggregate(indicator_task_target=Avg('indicator_task_target'))
        querySetPerformanceIndicatorTaskBenchmark = PerformanceIndicatorTaskBenchmark.objects.filter(piid=filter_indicator,taid__in=filter_tasks).aggregate(indicator_task_benchmark=Avg('indicator_task_benchmark'))
    else:
        # correct sum:
        #SELECTSTR = "SELECT `pivid`, `piid_id`, `icid_id`, `mid_id`, `thid_id`, `taid_id`, `uid_id`, sum(`indicator_value`), max(`indicator_value_log_timestamp`) FROM `perform_performanceindicatorvalue` WHERE (`piid_id` = %s AND `uid_id` IN (%s) AND  `mid_id` IN (%s) AND `taid_id` IN (%s) AND `indicator_value_log_timestamp` >= '%s' AND `indicator_value_log_timestamp` <= '%s') group by `uid_id`,`mid_id`;"
        SELECTSTR = "SELECT `pivid`, `piid_id`, `icid_id`, `mid_id`, `thid_id`, `taid_id`, `uid_id`, sum(`indicator_value`) AS `indicator_value`, max(`indicator_value_log_timestamp`) AS `indicator_value_log_timestamp` FROM `perform_performanceindicatorvalue` WHERE (`piid_id` = %s AND `uid_id` IN (%s) AND  `mid_id` IN (%s) AND `taid_id` IN (%s)) group by `uid_id`,`mid_id`;"
        querySetPerformanceIndicatorTaskTarget = PerformanceIndicatorTaskTarget.objects.filter(piid=filter_indicator,taid__in=filter_tasks).aggregate(indicator_task_target=Sum('indicator_task_target'))
        querySetPerformanceIndicatorTaskBenchmark = PerformanceIndicatorTaskBenchmark.objects.filter(piid=filter_indicator,taid__in=filter_tasks).aggregate(indicator_task_benchmark=Sum('indicator_task_benchmark'))

    if querySetPerformanceIndicatorTaskTarget:
        logger.error("querySetPerformanceIndicatorTaskTarget" + str(querySetPerformanceIndicatorTaskTarget))
        logger.error("querySetPerformanceIndicatorTaskTarget"+str(querySetPerformanceIndicatorTaskTarget['indicator_task_target']))
    if querySetPerformanceIndicatorTaskBenchmark:
        logger.error("querySetPerformanceIndicatorTaskBenchmark" + str(querySetPerformanceIndicatorTaskBenchmark['indicator_task_benchmark']))
    querysetPerformanceIndicatorValuesRAW = PerformanceIndicatorValue.objects.raw(SELECTSTR % (filter_indicator, str(filter_users)[1:-1], str(filter_missions)[1:-1], str(filter_tasks)[1:-1]))
    #filter_indicator, str(filter_users)[1:-1], str(filter_missions)[1:-1], str(filter_tasks)[1:-1], filter_start_date, filter_end_date))
    logger.error('querysetPerformanceIndicatorValuesRAW:' + str(querysetPerformanceIndicatorValuesRAW))

    querysetPerformanceIndicatorValues = list(querysetPerformanceIndicatorValuesRAW)
    logger.error('querysetPerformanceIndicatorValues Here NOW:' + str(querysetPerformanceIndicatorValues))

    if len(querysetPerformanceIndicatorValues) < 1:
        response = JsonResponse({"error": "No data"})
        response.status_code = 400
        return response

    #querysetPerformanceIndicatorValues.order_by('indicator_value_log_timestamp')
    #querysetPerformanceIndicatorValues=querysetPerformanceIndicatorValues.annotate(sumtasks=Sum('taid'))
    #logger.error('querysetPerformanceIndicatorValues SQL query :' + str(querysetPerformanceIndicatorValues.query))
    #for X in querysetPerformanceIndicatorValues:
    #    logger.error('querysetPerformanceIndicatorValues annotate :'+ str(X.num_tasks))


    #sorted(chain(page_list, article_list, post_list),key=attrgetter('indicator_value_log_timestamp'))
    #querysetPerformanceIndicatorValues.objects.values('uid').annotate(indicator_value=sum('indicator_value')).order_by('indicator_value_log_timestamp')
    #querysetPerformanceIndicatorValues.values('uid', 'mid').annotate(indicator_value=Sum('indicator_value')).order_by('indicator_value_log_timestamp')
    #logger.error('querysetPerformanceIndicatorValues annotate :'+ str(querysetPerformanceIndicatorValues[1]))


    #data = [{name: 'Math', data: redLine},{name: 'Economics', data: greenLine},{name: 'History', data: blueLine}]
    #redLine=[{x: 0, y: 170},{x: 88, y: 170},{x: 178, y: 149},{x: 201, y: 106},{x: 287, y: 83},{x: 331, y: 105},{x: 353, y: 172},{x: 500, y: 219}]

    performance_indicator_values_x = []
    performance_indicator_values_y = []

    performance_indicator_values_objects = {}
    for querysetPerformanceIndicatorValue in querysetPerformanceIndicatorValues:
        performance_indicator_values_x.append(querysetPerformanceIndicatorValue.indicator_value_log_timestamp)
        performance_indicator_values_y.append(querysetPerformanceIndicatorValue.indicator_value)
        if querysetPerformanceIndicatorValue.uid.username in performance_indicator_values_objects:
            performance_indicator_values_objects[querysetPerformanceIndicatorValue.uid.username].append(
                {'x': querysetPerformanceIndicatorValue.indicator_value_log_timestamp.strftime("%Y-%m-%d %H:%M"),
                 'y': querysetPerformanceIndicatorValue.indicator_value})
        else:
            performance_indicator_values_objects[querysetPerformanceIndicatorValue.uid.username] = [
                {'x': querysetPerformanceIndicatorValue.indicator_value_log_timestamp.strftime("%Y-%m-%d %H:%M"),
                 'y': querysetPerformanceIndicatorValue.indicator_value}]



    performance_indicator_values_list=[]
    for key, val in performance_indicator_values_objects.items():
        performance_indicator_values_list.append({'name':key,'data':val})

    data = {}
    data['perform_ind_data'] = performance_indicator_values_list

    querySetUsers = User.objects.filter(id__in=filter_users)
    #querySetUserProfiles = Profile.objects.filter(user__in=filter_users)
    querySetMissions = Mission.objects.filter(mid__in=filter_missions)

    logger.error('querySetUsers:' + str(querySetUsers[0].username)+" "+ str(querySetUsers[0].first_name)+" "+ str(querySetUsers[0].username))
    #logger.error('querySetUserProfiles:' + str(querySetUserProfiles[0]))
    logger.error('querySetMissions:' + str(querySetMissions[0].mission_name))

    data['general_comment'] = ''


    if len(performance_indicator_values_x) > 1:
        data['perform_ind_txt'] = "<p>" + "During the period from " + performance_indicator_values_x[0].strftime("%H:%m %p %A, %B %d, %Y") + " to " + performance_indicator_values_x[-1].strftime("%H:%m %p %A, %B %d, %Y") + ", concerning the '" + querysetPerformanceIndicator.indicator_name  + "' indicator, for the selected "
    else:
        data['perform_ind_txt'] = "<p>" + "Concerning the '" + querysetPerformanceIndicator.indicator_name + "' indicator, for the selected "

    if len(filter_users) == 1:
        data['perform_ind_txt'] += "user: "+querySetUsers[0].first_name + " " + querySetUsers[0].last_name + " (" + querySetUsers[0].username +"), in the selected "
    else:
        data['perform_ind_txt'] += "users:" + "</p><ul>"
        for querySetUser in querySetUsers:
            data['perform_ind_txt'] += "<li>" + querySetUser.first_name + " " + querySetUser.last_name + " (" + querySetUser.username +")"+"</li>"
        data['perform_ind_txt'] += "</ul>" + "</p>" + "<p>" + "In the selected "

    if len(filter_missions) == 1:
        data['perform_ind_txt'] += "mission: "+querySetMissions[0].mission_name + ".</p>"
    else:
        data['perform_ind_txt'] += "missions:" + "</p><ul>"
        for querySetMission in querySetMissions:
            data['perform_ind_txt'] += "<li>" + querySetMission.mission_name + "</li>"
        data['perform_ind_txt'] += "</ul>" + "</p>"

    # a, b = linreg(X, Y):
    #slope, intercept = linreg( performance_indicator_values_x, performance_indicator_values_y)
    if len(performance_indicator_values_x) > 1:
        slope, intercept, avgY, minY, minYTime, maxY, maxYTime = linreg2(performance_indicator_values_x, performance_indicator_values_y)
        logger.error("Slope: " + str(slope)+"   intercept:"+str(intercept)+"    avg:"+str(avgY)+"    minY:"+str(minY)+"    minYTime:"+str(minYTime)+"    maxY:"+str(maxY)+"    maxYTime:"+str(maxYTime))

        '''
        Period
        Trend
        Higest value (best or worst)
        Lowest value (bestor worst)
        Compare: last data point to first data point
        Compare: last data point to last-1 data point 
        '''
        # "%H:%m %p %A, %B %d, %Y (%Z)"
        data['perform_ind_txt'] += "<p>Your "+("best" if querysetPerformanceIndicator.is_inverted else "worst")+" value is "+str(round(minY,1))+" "+querysetPerformanceIndicator.indicator_unit+" dated "+minYTime.strftime("%H:%m %p %A, %B %d, %Y")+". "
        data['perform_ind_txt'] += "While your "+("worst" if querysetPerformanceIndicator.is_inverted else "best")+" value is "+str(round(maxY,1))+" "+querysetPerformanceIndicator.indicator_unit+" dated "+maxYTime.strftime("%H:%m %p %A, %B %d, %Y")+".</p>"
        data['perform_ind_txt'] += "<p>Your average value is "+str(round(avgY,1))+" "+querysetPerformanceIndicator.indicator_unit+". "
        if querySetPerformanceIndicatorTaskBenchmark['indicator_task_benchmark']:
            data['perform_ind_txt'] += "The benchmark for this indicator is "+str(round(querySetPerformanceIndicatorTaskBenchmark['indicator_task_benchmark'],1))+" "+querysetPerformanceIndicator.indicator_unit+". "
            if avgY==querySetPerformanceIndicatorTaskBenchmark['indicator_task_benchmark']:
                data['perform_ind_txt'] += "Your average value equals the benchmark.</p>"
            elif avgY<querySetPerformanceIndicatorTaskBenchmark['indicator_task_benchmark']:
                data['perform_ind_txt'] += "Your average value is lower than the benchmark by "+str(round(100*abs((avgY-querySetPerformanceIndicatorTaskBenchmark['indicator_task_benchmark'])/querySetPerformanceIndicatorTaskBenchmark['indicator_task_benchmark']),1))+" %. "+("Keep the good work.</p>" if querysetPerformanceIndicator.is_inverted else "You need to work on increasing your average value.</p>")
            else:
                data['perform_ind_txt'] += "Your average value is higher than the benchmark by "+str(round(100*abs((avgY-querySetPerformanceIndicatorTaskBenchmark['indicator_task_benchmark'])/querySetPerformanceIndicatorTaskBenchmark['indicator_task_benchmark']),1))+" %. "+("You need to work on decreasing your average value.</p>" if querysetPerformanceIndicator.is_inverted else "Keep the good work.</p>")
        if querySetPerformanceIndicatorTaskTarget['indicator_task_target']:
            data['perform_ind_txt'] += "<p>The organisation has set a target for this indicator, which is "+str(round(querySetPerformanceIndicatorTaskTarget['indicator_task_target'],1))+" "+querysetPerformanceIndicator.indicator_unit+". "
            if avgY==querySetPerformanceIndicatorTaskTarget['indicator_task_target']:
                data['perform_ind_txt'] += "Your average value equals the target</p>"
            elif avgY<querySetPerformanceIndicatorTaskTarget['indicator_task_target']:
                data['perform_ind_txt'] += "Your average value is lower than the target by "+str(round(100*abs((avgY-querySetPerformanceIndicatorTaskTarget['indicator_task_target'])/querySetPerformanceIndicatorTaskTarget['indicator_task_target']),1))+" %. "+("Keep the good work.</p>" if querysetPerformanceIndicator.is_inverted else "You need to work on increasing your average value.</p>")
            else:
                data['perform_ind_txt'] += "Your average value is higher than the target by "+str(round(100*abs((avgY-querySetPerformanceIndicatorTaskTarget['indicator_task_target'])/querySetPerformanceIndicatorTaskTarget['indicator_task_target']),1))+" %. "+("You need to work on decreasing your average value.</p>" if querysetPerformanceIndicator.is_inverted else "Keep the good work.</p>")

        logger.error('querysetPerformanceIndicator.is_inverted:' + str(querysetPerformanceIndicator.is_inverted))
        if slope != float("inf"):
            if ((slope > 0 and not(querysetPerformanceIndicator.is_inverted)) or (slope < 0 and querysetPerformanceIndicator.is_inverted)):
                data['perform_ind_txt'] += "<p>When it comes to performance over time, as shown in the figure, your performance is enhancing.</p>"
            elif slope == 0:
                data['perform_ind_txt'] += "<p>When it comes to performance over time, as shown in the figure, your performance is neither enhancing nor deteriorating.</p>"
            else:
                data['perform_ind_txt'] += "<p>When it comes to performance over time, as shown in the figure, your performance is deteriorating.</p>"
    elif len(performance_indicator_values_x) == 1:
        # only 1 point
        data['perform_ind_txt'] += "<p>Your indicator value is "+str(round(performance_indicator_values_y[0],1))+" "+querysetPerformanceIndicator.indicator_unit+". "
        if querySetPerformanceIndicatorTaskBenchmark:
            data['perform_ind_txt'] += "The benchmark for this indicator is "+str(round(querySetPerformanceIndicatorTaskBenchmark['indicator_task_benchmark'],1))+" "+querysetPerformanceIndicator.indicator_unit+". "
            if performance_indicator_values_y[0]==querySetPerformanceIndicatorTaskBenchmark['indicator_task_benchmark']:
                data['perform_ind_txt'] += "Your indicator value equals the benchmark.</p>"
            elif performance_indicator_values_y[0]<querySetPerformanceIndicatorTaskBenchmark['indicator_task_benchmark']:
                data['perform_ind_txt'] += "Your indicator value is lower than the benchmark by "+str(round(100*abs((performance_indicator_values_y[0]-querySetPerformanceIndicatorTaskBenchmark['indicator_task_benchmark'])/querySetPerformanceIndicatorTaskBenchmark['indicator_task_benchmark']),1))+" %. "+("Keep the good work.</p>" if querysetPerformanceIndicator.is_inverted else "You need to work on increasing your indicator value.</p>")
            else:
                data['perform_ind_txt'] += "Your indicator value is higher than the benchmark by "+str(round(100*abs((performance_indicator_values_y[0]-querySetPerformanceIndicatorTaskBenchmark['indicator_task_benchmark'])/querySetPerformanceIndicatorTaskBenchmark['indicator_task_benchmark']),1))+" %. "+("You need to work on decreasing your indicator value.</p>" if querysetPerformanceIndicator.is_inverted else "Keep the good work.</p>")
        if querySetPerformanceIndicatorTaskTarget:
            data['perform_ind_txt'] += "<p>The organisation has set a target for this indicator, which is "+str(round(querySetPerformanceIndicatorTaskTarget['indicator_task_target'],1))+" "+querysetPerformanceIndicator.indicator_unit+". "
            if performance_indicator_values_y[0]==querySetPerformanceIndicatorTaskTarget['indicator_task_target']:
                data['perform_ind_txt'] += "Your indicator value equals the target.</p>"
            elif performance_indicator_values_y[0]<querySetPerformanceIndicatorTaskTarget['indicator_task_target']:
                data['perform_ind_txt'] += "Your indicator value is lower than the target by "+str(round(100*abs((performance_indicator_values_y[0]-querySetPerformanceIndicatorTaskTarget['indicator_task_target'])/querySetPerformanceIndicatorTaskTarget['indicator_task_target']),1))+" %. "+("Keep the good work.</p>" if querysetPerformanceIndicator.is_inverted else "You need to work on increasing your indicator value.</p>")
            else:
                data['perform_ind_txt'] += "Your indicator value is higher than the target by "+str(round(100*abs((performance_indicator_values_y[0]-querySetPerformanceIndicatorTaskTarget['indicator_task_target'])/querySetPerformanceIndicatorTaskTarget['indicator_task_target']),1))+" %. "+("You need to work on decreasing your indicator value.</p>" if querysetPerformanceIndicator.is_inverted else "Keep the good work.</p>")
    elif len(performance_indicator_values_x) == 0:
        # only 0 point
        data['perform_ind_txt'] += "<p>You have not logged any values in relation to this indicator.</p>"


    logger.error('data[perform_ind_txt]:' + data['perform_ind_txt'])

    response = JsonResponse(data, safe=False)
    response.status_code = 201
    return response


@login_required(login_url='/accounts/login/')
def sop_items_data(request):
    logger = logging.getLogger(__name__)
    #data = request.cleaned_data["GET"]

    filter_mission = int(request.GET.get("filter_mission"))
    #filter_team = request.GET.get("filter_team")# teams__team_members=filter_team
    filter_country = '*'#request.GET.get("filter_country")
    filter_location = '*'#request.GET.get("filter_location")
    filter_attack_context = '*'#request.GET.get("filter_attack_context")
    filter_means_of_attack = '*'#request.GET.get("filter_means_of_attack")

    '''
    querysetSopsPolicies = Sop_policy.objects.filter(Location=filter_location,
                                                        Attack_context=filter_attack_context,
                                                        Means_of_attack=filter_means_of_attack,
											            Country=filter_country)
    '''
    querysetSopsPoliciesSurveyAnswer = Sop_policySurveyAnswer.objects.filter(mid=filter_mission,
                                                     Location=filter_location,
                                                     Attack_context=filter_attack_context,
                                                     Means_of_attack=filter_means_of_attack,
                                                     Country=filter_country)
    if querysetSopsPoliciesSurveyAnswer.exists():
        response = JsonResponse({"error": "you have filled this before"})
        response.status_code = 403  # To announce that the user isn't allowed to publish
        return response

    querysetSopsPolicies = Sop_policy.objects.all()

    sops_policies_list = []
    for querysetSopPolicy in querysetSopsPolicies:
        sops_policies_list.append({
            'Tag': querysetSopPolicy.Tag,
            'spid': querysetSopPolicy.spid,
            #'Measure_description': querysetSopPolicy.Measure_family+" > "+querysetSopPolicy.Measure_type+" > "+querysetSopPolicy.Measure_description,
            'Measure_description': querysetSopPolicy.Measure_type+" > "+querysetSopPolicy.Measure_description,
            'Prerequesit_sop_policy': querysetSopPolicy.Prerequesit_sop_policy,
            'Ds_level': querysetSopPolicy.Ds_level,
            'Implementation_stage': querysetSopPolicy.Implementation_stage,
        })
        logger.error('SOPs Policy item: ' + str(querysetSopPolicy.Measure_family))
    #logger.error('SOPs Policies List: ' + str(sops_policies_list))

    response = JsonResponse(sops_policies_list, safe=False)
    response.status_code = 201
    return response

@login_required(login_url='/accounts/login/')
def sop_entry_data(request):
    logger = logging.getLogger(__name__)
    #data = request.cleaned_data["GET"]

    filter_mission = int(request.GET.get("filter_mission"))
    #filter_team = request.GET.get("filter_team")# teams__team_members=filter_team
    filter_country = '*'#request.GET.get("filter_country")
    filter_location = '*'#request.GET.get("filter_location")
    filter_attack_context = '*'#request.GET.get("filter_attack_context")
    filter_means_of_attack = '*'#request.GET.get("filter_means_of_attack")
    questions_answers = json.loads(request.GET.get("questions_answers"))
    logger.error('SOPs questions_answers : ' + str(questions_answers))

    UserName = request.user.username;
    M = Mission.objects.filter(mid=filter_mission)[0]
    A = Sop_policySurveyAnswer.objects.create(mid=M,
                                        uid=request.user,
                                        Country=filter_country,
                                        Location=filter_location,
                                        Attack_context=filter_attack_context,
                                        Means_of_attack=filter_means_of_attack)
    A.save()
    for key, val in questions_answers.items():
        logger.error("key: " + str(key)+"-- val: " + str(key))
        Q = Sop_policy.objects.filter(spid=int(key))[0]
        F = Sop_policySurveyQuestionAnswer.objects.create(spsaid=A,
                                                    spid=Q,
                                                    answer_value=val)
        F.save()

    return HttpResponse("Success: " + UserName)



