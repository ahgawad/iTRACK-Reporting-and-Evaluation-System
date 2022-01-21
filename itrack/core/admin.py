from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_itrackuid')
    list_select_related = ('profile', )
    '''
    def get_location(self, instance):
        return instance.profile.location
    get_location.short_description = 'Location'
    '''
    def get_itrackuid(self, instance):
        return instance.profile.itrackuid
    get_itrackuid.short_description = 'iTRACK User ID'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Team)

admin.site.register(Threat)

admin.site.register(Mission)
admin.site.register(Phase)
admin.site.register(Task)

admin.site.register(ITRACKComponent)
admin.site.register(ITRACKComponentVersion)

admin.site.register(Setting)
