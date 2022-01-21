from django.db import models
from django.contrib.auth.models import User

# Add recognized model option to django
import django.db.models.options as options
#options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('usrdb',)

class UserSurvey(models.Model):
    usid = models.AutoField('User Survey ID', primary_key=True)
    survey_name = models.CharField(max_length=200)
    question_min_value = models.IntegerField(default=1)
    question_max_value = models.IntegerField(default=9)
    def __str__(self):
       return 'User Survey: ' + str(self.survey_name)

class UserSurveyQuestionConstruct(models.Model):
    usqcid = models.AutoField('User Survey Question Construct ID', primary_key=True)
    construct_text = models.CharField(max_length=200)
    def __str__(self):
       return str(self.construct_text)

class UserSurveyQuestion(models.Model):
    usqid = models.AutoField('User Survey Question ID', primary_key=True)
    usid = models.ForeignKey(UserSurvey, on_delete=models.CASCADE)
    usqcid = models.ForeignKey(UserSurveyQuestionConstruct, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    question_min_text = models.CharField(max_length=200,default='Unlikely')
    question_max_text = models.CharField(max_length=200,default='Likely')

    def __str__(self):
       return 'Survey: '+ str(self.usid)+'Question: ' + str(self.question_text)

class UserSurveyAnswer(models.Model):
    usaid = models.AutoField('User Survey Answer ID', primary_key=True)
    usid = models.ForeignKey(UserSurvey, on_delete=models.CASCADE)
    #uid = models.ForeignKey(User, on_delete=models.CASCADE)
    uid = models.ForeignKey(User, blank=True, null=True)
    icid = models.ForeignKey('core.iTRACKComponent', on_delete=models.CASCADE)
    icvid = models.ForeignKey('core.ITRACKComponentVersion', on_delete=models.CASCADE)
    answer_timestamp = models.DateTimeField(auto_now_add=True)

    ### relationship to the default database??
    #uid = models.ForeignKey(User, unique=True)
    #uid = models.OneToOneField(User)
    #uid = models.ForeignKey(User, on_delete=models.CASCADE)
    ###
    def __str__(self):
       return 'Survey: ' + str(self.usid) + ' answers of user: ' + str(self.uid)


class UserSurveyQuestionAnswer(models.Model):
    usqaid = models.AutoField('User Survey Question Answer ID', primary_key=True)
    usaid = models.ForeignKey(UserSurveyAnswer, on_delete=models.CASCADE)
    usqid = models.ForeignKey(UserSurveyQuestion, on_delete=models.CASCADE)
    answer_value = models.IntegerField(default=0)
