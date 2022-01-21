class DevelopRouters(object):
    def db_for_read(self,model, **hints):
        if model._meta.app_label == 'develop':
            return 'sftdb'
        return None

    def db_for_write(self,model, **hints):
        if model._meta.app_label == 'develop':
            return 'sftdb'
        return None

    def allow_relation(self,obj1, obj2, **hints):
        if obj1._meta.app_label == 'develop' and \
           obj2._meta.app_label == 'develop':
           return True
        return None

'''
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'develop' and db == 'sftdb':
            return True
        else:
            if app_label == 'develop' and db == 'default':
                return False
        return None
'''