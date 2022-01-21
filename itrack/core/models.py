from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# User.date_joined
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    itrackuid = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Mission(models.Model):
    mid = models.AutoField('Mission ID', primary_key=True)
    itrackmid = models.CharField(max_length=50, blank=False, null=False)
    mission_name = models.CharField(max_length=50, blank=True, null=True)
    mission_info = models.CharField(max_length=500, blank=True, null=True)
    mission_leaders = models.ManyToManyField(User,related_name = 'mission_leader')# Mission owners/leaders #models.ForeignKey(User,related_name = 'owner') # the owner
    mission_members = models.ManyToManyField(User,related_name = 'mission_member')
    mission_start_date = models.DateTimeField(null=False, blank=False)
    mission_end_date = models.DateTimeField(null=False, blank=False)

    def __str__(self):
       return str(self.mission_name)


class Threat(models.Model):
    thid = models.AutoField('Threat ID', primary_key=True)
    itrackthid = models.CharField(max_length=50, blank=False, null=False)
    threat_info = models.CharField(max_length=500, blank=True, null=False)
    threat_start_date = models.DateTimeField(null=False, blank=False)
    threat_end_date = models.DateTimeField(null=False, blank=False)

    def __str__(self):
       return str(self.threat_info)


class Team(models.Model):
    tid = models.AutoField('Team ID', primary_key=True)
    #itracktid = models.CharField(max_length=50, blank=False)
    team_name = models.CharField(max_length=50, blank=True, null=True)
    team_info = models.CharField(max_length=500, blank=True, null=True)
    team_leaders = models.ManyToManyField(User,related_name = 'team_leader')# Mission owners/leaders #models.ForeignKey(User,related_name = 'owner') # the owner
    team_members = models.ManyToManyField(User,related_name = 'team_member')
    def __str__(self):
       return str(self.team_name)


class ITRACKComponent(models.Model):
    # Table of software components
    icid = models.AutoField('iTRACK Component ID', primary_key=True)
    itrack_component_name = models.CharField(max_length=200)
    itrack_component_acr = models.CharField(max_length=5)
    def __str__(self):
       return str(self.itrack_component_name)


class ITRACKComponentVersion(models.Model):
    # Table of software components
    icvid = models.AutoField('iTRACK Component Version ID', primary_key=True)
    #icid = models.ForeignKey(ITRACKComponent, on_delete=models.CASCADE)
    itrack_component_version = models.CharField(max_length=50,null=False,blank=False)
    itrack_component_version_release_date = models.DateField(null=False, blank=False)
    def __str__(self):
       return str(self.itrack_component_version)


'''
class ITRACKComponentVersion(models.Model):
    # Table of software components
    icvid = models.AutoField('iTRACK Component ID', primary_key=True)
    icid = models.ForeignKey(ITRACKComponent, on_delete=models.CASCADE)
    itrack_component_version = models.IntegerField(default=1)
    def __str__(self):
       return str(self.icid) + ' Version: ' + str(self.itrack_component_version)
'''

class Task(models.Model):
    taid = models.AutoField('Task ID', primary_key=True)
    icid = models.ForeignKey(ITRACKComponent, on_delete=models.CASCADE)
    #pid = models.ForeignKey(Phase, blank=True, null=True)
    task_name = models.CharField(max_length=50)
    task_description = models.CharField(max_length=500)
    def __str__(self):
       return str(self.task_name)

class Phase(models.Model):
    pid = models.AutoField('Phase ID', primary_key=True)
    phase_name = models.CharField(max_length=50)
    phase_description = models.CharField(max_length=500)
    phase_tasks = models.ManyToManyField(Task,related_name = 'related_task')
    def __str__(self):
       return str(self.phase_name)



class Setting(models.Model):
    sid = models.AutoField('Phase ID', primary_key=True)
    setting_name = models.CharField(max_length=50, null=False, blank=False)
    setting_description = models.CharField(max_length=500)
    setting_value = models.FloatField(default=0, null=False, blank=False)
    #setting_value = models.DecimalField(decimal_places=2, max_digits=5, null=False, blank=False)

    def __str__(self):
       return str(self.setting_name)


