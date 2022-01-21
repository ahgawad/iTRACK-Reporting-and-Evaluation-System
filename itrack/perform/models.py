from django.db import models
from django.contrib.auth.models import User

#from develop import models as develop

# Add recognized model option to django
import django.db.models.options as options
#options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('pridb',)

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

class PerformanceIndicator(models.Model):
    piid = models.AutoField('Log Indicator ID', primary_key=True)
    indicator_name = models.CharField(max_length=200)
    indicator_unit = models.CharField(max_length=50)
    is_average = models.BooleanField(default=False)
    is_inverted = models.BooleanField(default=False)
    user_related = models.BooleanField(default=False)
    indicator_whereabouts = models.CharField(max_length=500) #where to find this indicator in the iTRACK database
    def __str__(self):
       return str(self.indicator_name)

class PerformanceIndicatorValue(models.Model):
    pivid = models.AutoField('Log Indicator Value ID', primary_key=True)
    piid = models.ForeignKey(PerformanceIndicator, on_delete=models.CASCADE)
    icid = models.ForeignKey('core.iTRACKComponent', on_delete=models.CASCADE)
    mid = models.ForeignKey('core.mission', blank=True, null=True)
    thid = models.ForeignKey('core.threat', blank=True, null=True)
    taid = models.ForeignKey('core.task', blank=True, null=True)
    uid = models.ForeignKey(User, blank=True, null=True)
    #indicator_value = models.IntegerField(default=0)
    indicator_value = models.FloatField(default=0, null=False, blank=False)
    # indicator_value = models.DecimalField(decimal_places=2, max_digits=5, default=0, null=False, blank=False)
    indicator_value_log_timestamp = models.DateTimeField(null=False, blank=False) #when it was logged originally
    def __str__(self):
       return 'Performance Indicator Value ID: ' + str(self.pivid)

    ### relationship to the default database??
    #uid = models.ForeignKey(User, unique=True)
    #uid = models.OneToOneField(User)
    #uid = models.ForeignKey(User, on_delete=models.CASCADE)
    ###

class PerformanceIndicatorTaskTarget(models.Model):
    pitid = models.AutoField('Log Indicator Target ID', primary_key=True)
    piid = models.ForeignKey(PerformanceIndicator, on_delete=models.CASCADE)
    taid = models.ForeignKey('core.task', blank=True, null=True)
    indicator_task_target = models.FloatField(default=0, null=False, blank=False)
    #indicator_task_target = models.DecimalField(decimal_places=2, max_digits=5, default=0, null=False, blank=False)
    def __str__(self):
       return 'Performance Indicator Target per Task ID: ' + str(self.pitid)

class PerformanceIndicatorTaskBenchmark(models.Model):
    pibid = models.AutoField('Log Indicator Benchmark ID', primary_key=True)
    piid = models.ForeignKey(PerformanceIndicator, on_delete=models.CASCADE)
    taid = models.ForeignKey('core.task', blank=True, null=True)
    indicator_task_benchmark = models.FloatField(default=0, null=False, blank=False)
    #indicator_task_benchmark = models.DecimalField(decimal_places=2, max_digits=5, default=0, null=False, blank=False)
    def __str__(self):
       return 'Performance Indicator Benchmark per Task ID: ' + str(self.pibid)


# SOPs ------------------ Start
# From Scenario Generator Start

class Sop_policy(models.Model):
    spid=models.AutoField('SOP Policy ID',primary_key=True)
    Tag=models.IntegerField(choices=keys_sop_policies_tags.items(), default='1', blank=False, null=False)
    Importance = models.IntegerField(choices=keys_sop_policies_importance_levels.items(), default='2', blank=False, null=False)
    Ds_level=models.CharField(max_length=1, choices=keys_sop_policies_ds_levels.items(), default='O')
    Sop_policy=models.CharField(max_length=1, choices=keys_sop_policies_types.items(), default='S')
    Sop_policy=models.CharField(max_length=50, blank=True, null=True)
    Measure_family=models.CharField(max_length=50, blank=True, null=True)
    Measure_type=models.CharField(max_length=50, blank=True, null=True)
    Measure_description=models.TextField(max_length=1000)
    Prerequesit_sop_policy=models.CharField(max_length=100, blank=True, null=True)
    Implementation_stage=models.CharField(max_length=1, choices=keys_sop_policies_implementation_stages.items(), default='P')
    #Damage_type=models.CharField(max_length=10, choices=keys_damage_types.items(), default='*')
    #Damage_mitigation_fraction=models.FloatField(default=0)
    Means_of_attack=models.CharField(max_length=10, choices=keys_means_of_attacks.items(), default='*')
    Attack_context=models.CharField(max_length=10, choices=keys_attack_contexts.items(), default='*')
    Location=models.CharField(max_length=10, choices=keys_locations.items(), default='*')
    Country=models.CharField(max_length=32, choices=keys_countries.items(), default='*')
    Mcda_criteria=models.CharField(max_length=50, blank=True, null=True)
    Mcda_points=models.IntegerField(default=0)
    Implementation_cost=models.IntegerField(default=0)
    Cost_type=models.CharField(max_length=1, choices=keys_sop_cost_types.items(), default='O')
    Measure_source=models.CharField(max_length=200, blank=True, null=True)

    def Damage_mitigation_type(self):
        # use reverse relation to get a list of all recorded numbers
        sop_policy_damage_mitigation_types=self.sop_policy_damage_mitigation_set.values_list('Damage_type', flat=True)
        sop_policy_damage_mitigation_types_count =self.sop_policy_damage_mitigation_set.count()
        return "This SOP/Policy has %s damage mitigation types recorded: %s" % (sop_policy_damage_mitigation_types_count, ', '.join(sop_policy_damage_mitigation_types))

    def __str__(self):
       return 'SOP/Policy ID: ' + str(self.spid)

    class Meta:
        verbose_name = 'SOP/Policy'
        verbose_name_plural = 'SOPs/Policies'

class Sop_policy_damage_mitigation(models.Model):
    spdmid=models.AutoField('Damage mitigation type ID',primary_key=True)

    Sop_policy=models.ForeignKey(Sop_policy, on_delete=models.CASCADE)

    Damage_type=models.CharField(max_length=10, choices=keys_damage_types.items(), default='*')
    Damage_mitigation_fraction=models.FloatField(default=0)

    def __str__(self):
       return 'SOP Policy Damage Mitigation Type ID: ' + str(self.spdmid)

# SOPs from Scenario Generator End
# SOPs New Start
class Sop_policySurveyAnswer(models.Model):
    spsaid = models.AutoField('SOPs/Policies Survey Answer ID', primary_key=True)
    mid = models.ForeignKey('core.Mission', on_delete=models.CASCADE)
    Means_of_attack=models.CharField(max_length=10, choices=keys_means_of_attacks_fixed.items(), default='AB')
    Attack_context=models.CharField(max_length=10, choices=keys_attack_contexts_fixed.items(), default='Am')
    Location=models.CharField(max_length=10, choices=keys_locations_fixed.items(), default='R')
    Country=models.CharField(max_length=32, choices=keys_countries_fixed.items(), default='syria')

    #uid = models.ForeignKey(User, on_delete=models.CASCADE)
    uid = models.ForeignKey(User, blank=True, null=True)

    answer_timestamp = models.DateTimeField(auto_now_add=True)

    ### relationship to the default database??
    #uid = models.ForeignKey(User, unique=True)
    #uid = models.OneToOneField(User)
    #uid = models.ForeignKey(User, on_delete=models.CASCADE)
    ###
    def __str__(self):
       return 'SOPs/Policies Survey Answer: ' + str(self.spsaid) + ' answers for mission: ' + str(self.mid)+ ' by user: ' + str(self.uid)


class Sop_policySurveyQuestionAnswer(models.Model):
    spsqaid = models.AutoField('SOPs Policyies Survey Question Answer ID', primary_key=True)
    spsaid = models.ForeignKey(Sop_policySurveyAnswer, on_delete=models.CASCADE)
    spid = models.ForeignKey(Sop_policy, on_delete=models.CASCADE)
    answer_value = models.BooleanField(default=False)

# SOPs New End
# SOPs ----End

