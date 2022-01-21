from django.db import models
# Add recognized model option to django
#import django.db.models.options as options
#options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('sftdb',)


class ITRACKComponentElement(models.Model):
    iceid = models.AutoField('iTRACK Component Element ID', primary_key=True)
    icid = models.ForeignKey('core.ITRACKComponent', on_delete=models.CASCADE)
    itrack_component_element_name = models.CharField(max_length=200)
    #itrack_component_element_version = models.IntegerField(default=1)
    def __str__(self):
       return str(self.itrack_component_element_name)

class ITRACKComponentDevelopmentIndicator(models.Model):
    # Table of indicators names
    iciid = models.AutoField('iTRACK Component Development Indicator ID', primary_key=True)
    indicator_name = models.CharField(max_length=200)
    is_percentage = models.BooleanField(default=False)
    def __str__(self):
       return str(self.indicator_name)

class ITRACKComponentIndicatorValue(models.Model):
    # Table of indicators values
    icivid = models.AutoField('iTRACK Component Development Indicator Value ID', primary_key=True)
    iciid = models.ForeignKey(ITRACKComponentDevelopmentIndicator, on_delete=models.CASCADE)
    icid = models.ForeignKey('core.ITRACKComponent', on_delete=models.CASCADE)
    icvid = models.ForeignKey('core.ITRACKComponentVersion', on_delete=models.CASCADE)
    indicator_value = models.FloatField(null=True, blank=True)
    #indicator_value = models.DecimalField(decimal_places=2,max_digits=5,null=True, blank=True)
    #indicator_details = models.TextField(max_length=2000, null=True)
    def __str__(self):
       return 'Indicator: ' + str(self.iciid)+' of Component: ' + str(self.icid)+' Version: ' + str(self.icvid)

class ITRACKComponentElementIndicatorValue(models.Model):
    # Table of indicators values
    iceivid = models.AutoField('iTRACK Component Element Development Indicator Value ID', primary_key=True)
    iciid = models.ForeignKey(ITRACKComponentDevelopmentIndicator, on_delete=models.CASCADE)
    # icid = models.ForeignKey(ITRACKComponent, on_delete=models.CASCADE)
    iceid = models.ForeignKey(ITRACKComponentElement, on_delete=models.CASCADE)
    icvid = models.ForeignKey('core.ITRACKComponentVersion', on_delete=models.CASCADE)
    indicator_value = models.FloatField(null=True, blank=True)
    #indicator_value = models.DecimalField(decimal_places=2,max_digits=5,null=True, blank=True)
    #indicator_details = models.TextField(max_length=2000, null=True)
    def __str__(self):
       return 'Indicator: ' + str(self.iciid)+' of Element: ' + str(self.iceid)+' Version: ' + str(self.icvid)
